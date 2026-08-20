"""
Download do dataset GitSkills (HuggingFace → Parquet local).

Fonte: https://huggingface.co/datasets/mvaccargiu/gitskills
Paper: arXiv:2608.10906

Uso:
    python scripts/download_dataset.py             # Baixa todas as tabelas
    python scripts/download_dataset.py artifacts    # Baixa apenas a tabela 'artifacts'
    python scripts/download_dataset.py repos        # Baixa apenas a tabela 'repos'
"""

import sys
import time
from pathlib import Path

from datasets import load_dataset

# ─── Configuração ───────────────────────────────────────────────────────────

HF_DATASET_ID = "mvaccargiu/gitskills"

TABLES = {
    "artifacts":         "Tabela principal — um registro por SKILL.md (~3.8M linhas, ~12 GB)",
    "artifact_siblings": "Scripts e arquivos junto às skills (~7.3M linhas, ~1 GB)",
    "repos":             "Metadados dos repositórios (~282K linhas, ~30 MB)",
    "mining_runs":       "Log de proveniência (7 linhas, ~5 KB)",
}

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ─── Funções ────────────────────────────────────────────────────────────────

def download_table(table_name: str) -> Path:
    """Baixa uma tabela do HuggingFace e salva como Parquet local."""
    output_path = DATA_DIR / f"{table_name}.parquet"

    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  ⏭️  {table_name}.parquet já existe ({size_mb:.1f} MB). Pulando.")
        return output_path

    print(f"  ⬇️  Baixando '{table_name}'...")
    print(f"     {TABLES[table_name]}")

    start = time.time()
    ds = load_dataset(HF_DATASET_ID, table_name, split="train")
    elapsed_download = time.time() - start

    print(f"     Download: {elapsed_download:.0f}s — {len(ds):,} registros carregados")
    print(f"     Salvando em {output_path}...")

    start = time.time()
    ds.to_parquet(str(output_path))
    elapsed_save = time.time() - start

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"     Salvo: {size_mb:.1f} MB em {elapsed_save:.0f}s")

    return output_path


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Determinar quais tabelas baixar
    if len(sys.argv) > 1:
        requested = sys.argv[1:]
        invalid = [t for t in requested if t not in TABLES]
        if invalid:
            print(f"❌ Tabela(s) inválida(s): {invalid}")
            print(f"   Tabelas disponíveis: {list(TABLES.keys())}")
            sys.exit(1)
        tables_to_download = requested
    else:
        tables_to_download = list(TABLES.keys())

    print(f"📦 GitSkills Dataset — Download via HuggingFace")
    print(f"   Fonte: {HF_DATASET_ID}")
    print(f"   Destino: {DATA_DIR}")
    print(f"   Tabelas: {tables_to_download}")
    print()

    for table_name in tables_to_download:
        download_table(table_name)
        print()

    print("✅ Download concluído!")
    print()

    # Resumo dos arquivos
    print("📊 Arquivos em data/:")
    for f in sorted(DATA_DIR.glob("*.parquet")):
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"   {f.name:30s} {size_mb:>10.1f} MB")


if __name__ == "__main__":
    main()
