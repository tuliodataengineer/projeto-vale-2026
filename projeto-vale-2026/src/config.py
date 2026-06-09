"""
config.py — Configuração central do projeto Vale 2026
Responsável: Cisquim

Todos os caminhos e constantes do projeto ficam aqui.
Nunca use caminhos hardcoded nos notebooks ou scripts — sempre importe deste arquivo.
"""

from pathlib import Path

# ─── RAIZ DO PROJETO ──────────────────────────────────────────────────────────
# Ajusta automaticamente independente de onde o script é chamado
ROOT = Path(__file__).resolve().parent.parent

# ─── DADOS ────────────────────────────────────────────────────────────────────
DATA_RAW       = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"

# Telemetria (arquivos brutos da Vale — nunca editar)
TELEMETRIA_JAN = DATA_RAW / "telemetry_jan.parquet"
TELEMETRIA_FEV = DATA_RAW / "telemetry_feb.parquet"
TELEMETRIA_MAR = DATA_RAW / "telemetry_mar.parquet"
TELEMETRIA_ABR = DATA_RAW / "telemetry_abr.parquet"
TELEMETRIA_MAI = DATA_RAW / "telemetry_may.parquet"
TELEMETRIA_JUN = DATA_RAW / "telemetry_jun.parquet"

TELEMETRIA_FILES = [
    TELEMETRIA_JAN,
    TELEMETRIA_FEV,
    TELEMETRIA_MAR,
    TELEMETRIA_ABR,
    TELEMETRIA_MAI,
    TELEMETRIA_JUN,
]

# Apontamentos
APONTAMENTOS_RAW = DATA_RAW / "desenvolver_apontamentos.parquet"

# Regras de negócio
ALARMES_REGRAS = DATA_RAW / "Alarmes - Regra de Negocio.xlsx"
DICIONARIO     = DATA_RAW / "Dicionario_Dados.xlsx"

# ─── DADOS PROCESSADOS ────────────────────────────────────────────────────────
TELEMETRIA_LIMPA     = DATA_PROCESSED / "telemetria_limpa.parquet"
APONTAMENTOS_LIMPOS  = DATA_PROCESSED / "apontamentos_limpos.parquet"
TELEMETRIA_FEATURES  = DATA_PROCESSED / "telemetria_features.parquet"

# ─── NOTEBOOKS ────────────────────────────────────────────────────────────────
NOTEBOOKS = ROOT / "notebooks"

# ─── SRC ──────────────────────────────────────────────────────────────────────
SRC = ROOT / "src"

# ─── DASHBOARD ────────────────────────────────────────────────────────────────
DASHBOARD = ROOT / "dashboard"

# ─── RELATÓRIO ────────────────────────────────────────────────────────────────
RELATORIO = ROOT / "relatorio"

# ─── CONSTANTES DO NEGÓCIO ────────────────────────────────────────────────────

# Coluna target
TARGET = "Is_Dont_Go"

# Colunas de identidade do equipamento
COL_TAG_TELEMETRIA    = "TAG"
COL_TAG_APONTAMENTOS  = "Tag"
COL_TIMESTAMP         = "Data_Evento"
COL_ALARME            = "Alarme"
COL_CRITICIDADE       = "Criticidade"

# Colunas a descartar na modelagem (zero variância ou identificadores)
COLUNAS_DESCARTAR = [
    "Id_Eventos_Telemetria",  # ID único — não agrega
    "Localidade",             # Sempre "Itabira" — zero variância
    "Matricula_Operador_Hash",# Redundante com Nome_Operador_Anon
    "Id_Alarme",              # ID numérico do alarme — usar nome
    "Id_Criticidade",         # ID numérico — usar texto
]

# Níveis de criticidade normalizados
CRITICIDADE_MAP = {
    "informacional" : "Informacional",
    "não crítico"   : "Nao_Critico",
    "nao critico"   : "Nao_Critico",
    "n??o crítico"  : "Nao_Critico",
    "não cr??tico"  : "Nao_Critico",
    "critico"       : "Critico",
    "crítico"       : "Critico",
}

# Janelas de rolling (em número de eventos por equipamento)
ROLLING_WINDOWS = [10, 50, 100]  # ajustar após ver granularidade real

# Janela de predição: alertas nas próximas N horas
JANELA_PREDICAO_HORAS = 4

# Turnos
TURNO_DIA   = "dia"    # Início às 06:00
TURNO_NOITE = "noite"  # Início às 18:00

# ─── UTILITÁRIO ───────────────────────────────────────────────────────────────
def verificar_estrutura():
    """Verifica se as pastas necessárias existem e cria as que faltam."""
    pastas = [DATA_RAW, DATA_PROCESSED, NOTEBOOKS, SRC, DASHBOARD, RELATORIO]
    for pasta in pastas:
        pasta.mkdir(parents=True, exist_ok=True)
    print("✅ Estrutura de pastas verificada com sucesso.")
    print(f"   ROOT: {ROOT}")


if __name__ == "__main__":
    verificar_estrutura()
    print("\n📂 Caminhos configurados:")
    print(f"   data/raw        → {DATA_RAW}")
    print(f"   data/processed  → {DATA_PROCESSED}")
    print(f"   notebooks       → {NOTEBOOKS}")
    print(f"   src             → {SRC}")
    print(f"   dashboard       → {DASHBOARD}")
    print(f"   relatorio       → {RELATORIO}")
