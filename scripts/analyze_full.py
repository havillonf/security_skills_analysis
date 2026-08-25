import duckdb
import os
import re

def run_analysis():
    print("Iniciando análise com DuckDB...")
    conn = duckdb.connect()
    
    conn.execute("CREATE VIEW artifacts AS SELECT * FROM read_parquet('data/artifacts.parquet')")
    conn.execute("CREATE VIEW repos AS SELECT * FROM read_parquet('data/repos.parquet')")
    
    # 39 keywords de segurança do notebook 1
    security_keywords = [
        'security', 'secure', 'vulnerability', 'exploit',
        'authentication', 'authorization', 'auth',
        'encryption', 'encrypt', 'decrypt',
        'injection', 'xss', 'csrf', 'sql injection',
        'sanitize', 'sanitization', 'validate', 'validation',
        'dependency', 'supply chain', 'audit',
        'secret', 'credential', 'token', 'api key', 'password',
        'prompt injection', 'jailbreak', 'guardrail',
        'safety', 'harmful', 'malicious',
        'owasp', 'cve', 'penetration', 'pentest',
        'firewall', 'sandbox', 'permission'
    ]
    
    # Para regex no DuckDB (regexp_matches)
    # Apenas como curiosidade, DuckDB usa re2. Palavras pequenas devem ter \b
    def make_pattern(kws):
        parts = []
        for kw in kws:
            if len(kw) <= 4:
                parts.append(r'\b' + kw + r'\b')
            else:
                parts.append(kw)
        return '(?i)(' + '|'.join(parts) + ')'
    
    sec_pattern = make_pattern(security_keywords)
    privacy_pattern = r'(?i)\b(LGPD|GDPR|PII|privacy|data protection)\b'
    exec_pattern = r'(?i)\b(subprocess|shell|curl|pip install|exec|wget)\b'
    
    # Cria uma view enriquecida com flags de segurança
    # Coalesce para evitar NULLs que atrapalham o regexp_matches
    conn.execute(f"""
        CREATE VIEW enriched_artifacts AS 
        SELECT 
            a.*,
            r.language,
            regexp_matches(COALESCE(a.content, ''), '{sec_pattern}') AS sec_in_content,
            regexp_matches(COALESCE(a.description, ''), '{sec_pattern}') AS sec_in_desc,
            regexp_matches(COALESCE(a.name, ''), '{sec_pattern}') AS sec_in_name,
            regexp_matches(COALESCE(a.filename, ''), '{sec_pattern}') AS sec_in_filename,
            regexp_matches(COALESCE(a.content, '') || ' ' || COALESCE(a.description, '') || ' ' || COALESCE(a.name, ''), '{privacy_pattern}') AS has_privacy,
            regexp_matches(COALESCE(a.content, ''), '{exec_pattern}') AS has_exec
        FROM artifacts a
        LEFT JOIN repos r ON a.repo_full_name = r.full_name
    """)
    
    conn.execute("""
        CREATE VIEW artifacts_flags AS
        SELECT
            *,
            (sec_in_content OR sec_in_desc OR sec_in_name) AS is_security,
            (sec_in_name OR sec_in_filename) AS is_named_security
        FROM enriched_artifacts
    """)
    
    # 1. Achados-chave
    print("Calculando achados gerais...")
    distinct_skills = conn.execute("SELECT count(DISTINCT file_sha) FROM artifacts_flags").fetchone()[0]
    sec_skills = conn.execute("SELECT count(DISTINCT file_sha) FROM artifacts_flags WHERE is_security").fetchone()[0]
    sec_in_desc = conn.execute("SELECT count(DISTINCT file_sha) FROM artifacts_flags WHERE sec_in_desc").fetchone()[0]
    sec_only_body = conn.execute("SELECT count(DISTINCT file_sha) FROM artifacts_flags WHERE is_security AND NOT sec_in_desc AND NOT sec_in_name").fetchone()[0]
    sec_with_scripts = conn.execute("SELECT count(DISTINCT file_sha) FROM artifacts_flags WHERE is_security AND has_scripts = 1").fetchone()[0]
    sec_with_exec = conn.execute("SELECT count(DISTINCT file_sha) FROM artifacts_flags WHERE is_security AND has_exec").fetchone()[0]
    privacy_skills = conn.execute("SELECT count(DISTINCT file_sha) FROM artifacts_flags WHERE has_privacy").fetchone()[0]
    named_sec = conn.execute("SELECT count(DISTINCT file_sha) FROM artifacts_flags WHERE is_named_security").fetchone()[0]
    
    # 2. Tamanho
    print("Calculando tamanho...")
    size_stats = conn.execute("""
        SELECT 
            is_security,
            count(DISTINCT file_sha) as cnt,
            avg(body_chars) as avg_body,
            sum(has_scripts)*100.0/count(*) as pct_scripts,
            sum(has_references)*100.0/count(*) as pct_refs
        FROM (SELECT file_sha, arg_max(is_security, discovered_at) as is_security, avg(body_chars) as body_chars, max(has_scripts) as has_scripts, max(has_references) as has_references FROM artifacts_flags GROUP BY file_sha)
        GROUP BY is_security
        ORDER BY is_security DESC
    """).fetchall()
    
    # 3. Segurança por Linguagem
    print("Calculando por linguagem...")
    langs = ['Java', 'Go', 'PHP', 'C#', 'Python', 'Shell', 'TypeScript', 'JavaScript', 'Rust', 'Swift']
    lang_stats = conn.execute(f"""
        SELECT 
            language,
            count(DISTINCT CASE WHEN is_security THEN file_sha END) as sec_count,
            count(DISTINCT file_sha) as total_count
        FROM artifacts_flags
        WHERE language IN ({','.join(['?']*len(langs))})
        GROUP BY language
        ORDER BY sec_count DESC
    """, langs).fetchall()
    
    # 4. Mais copiadas
    print("Calculando mais copiadas...")
    top_copied = conn.execute("""
        SELECT 
            COALESCE(name, filename) as skill_name,
            count(*) as copies
        FROM artifacts_flags
        WHERE is_security
        GROUP BY file_sha, COALESCE(name, filename)
        ORDER BY copies DESC
        LIMIT 10
    """).fetchall()
    
    # 5. Tópicos por Linguagem
    print("Calculando tópicos por linguagem...")
    topics = {
        'secret': ['secret', 'credential', 'token', 'api key', 'password'],
        'authentication': ['authentication', 'auth'],
        'authorization': ['authorization'],
        'injection': ['injection', 'sql injection'],
        'guardrail': ['guardrail'],
        'vulnerability': ['vulnerability', 'exploit'],
        'encryption': ['encryption', 'encrypt', 'decrypt'],
        'owasp': ['owasp'],
        'prompt_injection': ['prompt injection'],
        'xss': ['xss'],
        'csrf': ['csrf'],
        'sanitize': ['sanitize', 'sanitization', 'validate', 'validation']
    }
    
    target_langs = ['Python', 'TypeScript', 'JavaScript', 'Go', 'Java', 'Rust']
    topic_results = []
    
    for t_name, t_kws in topics.items():
        pat = make_pattern(t_kws)
        row = [t_name]
        for lang in target_langs:
            cnt = conn.execute(f"""
                SELECT count(DISTINCT file_sha) 
                FROM artifacts_flags 
                WHERE language = ? AND regexp_matches(COALESCE(content, '') || ' ' || COALESCE(description, '') || ' ' || COALESCE(name, ''), ?)
            """, [lang, pat]).fetchone()[0]
            row.append(cnt)
        topic_results.append(row)
        
    print("Gerando Markdown...")
    
    md = f"""# Questões de Pesquisa — Segurança em Agent Skills (Dataset Completo)

> Análise sobre o dataset GitSkills completo (~3.8M artifacts), recriando as métricas exploratórias com o poder do DuckDB.

---

## Achados-Chave no Dataset Completo

| Métrica | Valor |
|---------|-------|
| Skills distintas (file_sha único) | {distinct_skills:,} |
| Skills que mencionam **ao menos 1** termo de segurança | **{sec_skills:,} ({sec_skills/distinct_skills*100:.1f}%)** |
| Skills cuja **description** menciona segurança | **{sec_in_desc:,} ({sec_in_desc/distinct_skills*100:.1f}%)** |
| Skills que mencionam segurança **só no body** | **{sec_only_body:,} ({sec_only_body/distinct_skills*100:.1f}%)** |
| Skills de segurança com **scripts bundled** (executáveis) | **{sec_with_scripts:,}** |
| Skills de segurança com instruções de **execução de comandos** | **{sec_with_exec:,}** |
| Skills sobre **privacidade/compliance** (LGPD, GDPR, PII) | **{privacy_skills:,}** |
| Skills nomeadas explicitamente com termos de segurança | **{named_sec:,}** |

### Tamanho: Security vs Non-Security

| Categoria | Count | Avg body (chars) | % com scripts | % com referências |
|-----------|-------|-------------------|---------------|-------------------|
"""
    for r in size_stats:
        cat = "**security**" if r[0] else "non_security"
        md += f"| {cat} | {r[1]:,} | {r[2]:.0f} | {r[3]:.1f}% | {r[4]:.1f}% |\n"

    md += """
### Segurança por Linguagem

| Linguagem | Skills de Segurança | Total Skills | **% Segurança** |
|-----------|---------------------|--------------|-----------------|
"""
    for r in lang_stats:
        pct = (r[1] / r[2] * 100) if r[2] > 0 else 0
        md += f"| {r[0]} | {r[1]:,} | {r[2]:,} | **{pct:.1f}%** |\n"
        
    md += """
### Skills de Segurança Mais Copiadas (Top 10)

| Skill (Nome / Filename) | Cópias |
|-------------------------|--------|
"""
    for r in top_copied:
        md += f"| {r[0]} | {r[1]} |\n"
        
    md += """
### Tópicos de Segurança por Linguagem

| Tópico | Python | TypeScript | JavaScript | Go | Java | Rust |
|--------|--------|------------|------------|-----|------|------|
"""
    for r in topic_results:
        md += f"| {r[0]} | {r[1]:,} | {r[2]:,} | {r[3]:,} | {r[4]:,} | {r[5]:,} | {r[6]:,} |\n"
        
    # Copiando as RQs do doc original
    md += """
---

## Questões de Pesquisa Propostas

*(As questões abaixo permanecem as mesmas do planejamento original, agora embasadas pelos dados do dataset completo).*

### RQ1 — Prevalência e Propósito
**Qual a prevalência de skills agênticas dedicadas à segurança no ecossistema GitHub, e qual proporção trata segurança como propósito central versus menção incidental?**

**Subquestões:**
- RQ1.1: Qual a proporção de skills cujo **propósito principal** é segurança vs. skills que **mencionam** segurança apenas no corpo das instruções?
- RQ1.2: Existem padrões textuais que permitam distinguir automaticamente skills "security-first" de skills que apenas mencionam segurança superficialmente?

---

### RQ2 — Cobertura Temática e Lacunas
**Quais domínios de segurança são cobertos pelas skills agênticas, e quais estão sub-representados ou ausentes?**

**Subquestões:**
- RQ2.1: Quais categorias da OWASP Top 10 (web e LLM) estão representadas nas skills, e quais estão ausentes?
- RQ2.2: Existem domínios de segurança específicos ao contexto de agentes de IA (prompt injection, guardrails, sandboxing) adequadamente cobertos?
- RQ2.3: A cobertura de tópicos de segurança varia conforme a linguagem de programação do repositório?

---

### RQ3 — Similaridade Semântica e Sintática
**As skills de segurança apresentam convergência semântica ou sintática, indicando a emergência de padrões ou templates?**

**Subquestões:**
- RQ3.1: Quais clusters semânticos emergem ao agrupar skills de segurança por embeddings do texto?
- RQ3.2: Existe convergência sintática (estrutura, seções, checklists) entre skills de segurança de diferentes repositórios e linguagens?
- RQ3.3: As skills copiadas mantêm fidelidade ao conteúdo original ou sofrem modificações que alteram o comportamento de segurança?

---

### RQ4 — Segurança por Linguagem de Programação
**Como a presença e a qualidade de skills de segurança variam entre diferentes linguagens de programação?**

**Subquestões:**
- RQ4.1: Existem diferenças significativas na proporção de skills de segurança entre linguagens?
- RQ4.2: Os **tópicos** de segurança cobertos variam por linguagem de forma consistente com as vulnerabilidades típicas daquela linguagem?
- RQ4.3: Linguagens com ecossistemas de segurança mais maduros possuem menos skills dedicadas a mitigar esses riscos?

---

### RQ5 — Supply Chain e Confiança
**Skills de segurança que incluem scripts executáveis representam um vetor de risco na cadeia de suprimentos de software?**

**Subquestões:**
- RQ5.1: Qual proporção de skills de segurança inclui scripts que executam comandos no sistema?
- RQ5.2: Cópias modificadas de skills populares introduzem capacidades de execução ou acesso à rede ausentes no original?
- RQ5.3: Existe correlação entre a popularidade de um repositório (stars) e a presença de skills com scripts executáveis?

---

### RQ6 — Autoria: Humanos vs. Agentes
**Skills de segurança escritas por agentes de IA diferem em qualidade ou cobertura das escritas por humanos?**

**Subquestões:**
- RQ6.1: Qual a proporção de skills de segurança criadas por bots vs. humanos?
- RQ6.2: Skills de segurança criadas por bots diferem em tamanho, cobertura temática ou estrutura das criadas por humanos?
- RQ6.3: Skills criadas por agentes tendem a ser mais genéricas ou específicas?

---

### RQ7 — Compliance e Regulamentação
**As skills agênticas abordam adequadamente requisitos regulatórios como LGPD, GDPR e frameworks de compliance?**

**Subquestões:**
- RQ7.1: Quais frameworks regulatórios são mencionados nas skills e com que profundidade?
- RQ7.2: Skills que mencionam compliance fornecem instruções acionáveis ou apenas citam o framework superficialmente?
"""

    with open('docs/research_questions_full_dataset.md', 'w') as f:
        f.write(md)
        
    print("Processo concluído! Arquivo gerado em docs/research_questions_full_dataset.md")

if __name__ == "__main__":
    run_analysis()
