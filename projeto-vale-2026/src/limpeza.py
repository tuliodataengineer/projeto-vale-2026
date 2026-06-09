"""
limpeza.py — Funções de limpeza e pré-processamento — Vale 2026
Responsável: Cisquim

Todas as transformações documentadas com ANTES/DEPOIS
conforme exigido pelo Estudo Guiado (CM 3.1).
"""

import pandas as pd
import numpy as np
from pathlib import Path


# ─── TELEMETRIA ───────────────────────────────────────────────────────────────

def carregar_telemetria_completa(arquivos: list, verbose: bool = True) -> pd.DataFrame:
    """
    Carrega todos os parquets de telemetria em um único DataFrame.

    Parâmetros
    ----------
    arquivos : list de Path ou str
        Lista com os caminhos dos arquivos .parquet mensais.
    verbose : bool
        Se True, imprime progresso do carregamento.

    Retorna
    -------
    pd.DataFrame com toda a telemetria concatenada.
    """
    dfs = []
    for arq in arquivos:
        arq = Path(arq)
        if not arq.exists():
            print(f"  ⚠️  Arquivo não encontrado: {arq.name} — pulando.")
            continue
        df = pd.read_parquet(arq)
        if verbose:
            dg = df["Is_Dont_Go"].sum()
            print(f"  ✅ {arq.name}: {len(df):>12,} linhas | Don't Go: {dg:>5,} ({dg/len(df)*100:.4f}%)")
        dfs.append(df)

    if not dfs:
        raise FileNotFoundError("Nenhum arquivo de telemetria encontrado.")

    df_total = pd.concat(dfs, ignore_index=True)
    if verbose:
        print(f"\n  📦 TOTAL: {len(df_total):,} linhas | {df_total['Is_Dont_Go'].sum():,} Don't Go")
    return df_total


def normalizar_criticidade(df: pd.DataFrame, col: str = "Criticidade") -> pd.DataFrame:
    """
    Normaliza a coluna Criticidade corrigindo problemas de encoding UTF-8.

    ANTES: 'Não Crítico', 'N??o Crítico', 'Não Cr??tico' (3 variantes)
    DEPOIS: 'Nao_Critico' (1 variante padronizada)

    Controle de Alterações
    ----------------------
    Campo       : Criticidade
    Problema    : Encoding quebrado — caracteres especiais corrompidos
    Qtd aprox.  : ~11 registros afetados (Jan) — verificar total
    Tratamento  : str.normalize + mapeamento manual
    Justificativa: Garantir que value_counts() e groupby() funcionem corretamente
    """
    mapa = {
        "Informacional" : "Informacional",
        "Não Crítico"   : "Nao_Critico",
        "Nao Critico"   : "Nao_Critico",
        "N??o Crítico"  : "Nao_Critico",
        "Não Cr??tico"  : "Nao_Critico",
        "Critico"       : "Critico",
        "Crítico"       : "Critico",
    }

    antes = df[col].value_counts().to_dict()
    df[col] = (
        df[col]
        .str.strip()
        .map(lambda x: mapa.get(x, x))  # mantém valor original se não mapeado
    )
    depois = df[col].value_counts().to_dict()

    print(f"  🔧 Criticidade normalizada:")
    print(f"     ANTES : {antes}")
    print(f"     DEPOIS: {depois}")
    return df


def remover_colunas_inuteis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove colunas que não agregam valor à modelagem.

    Controle de Alterações
    ----------------------
    Localidade          : Sempre 'Itabira' — zero variância
    Id_Eventos_Telemetria: Identificador único — não é feature
    Id_Alarme           : ID numérico do alarme — nome já está em 'Alarme'
    Id_Criticidade      : ID numérico — texto já está em 'Criticidade'
    Matricula_Operador_Hash: Redundante com Nome_Operador_Anon
    """
    colunas_remover = [
        "Id_Eventos_Telemetria",
        "Localidade",
        "Id_Alarme",
        "Id_Criticidade",
        "Matricula_Operador_Hash",
    ]
    existentes = [c for c in colunas_remover if c in df.columns]
    df = df.drop(columns=existentes)
    print(f"  🗑️  Colunas removidas: {existentes}")
    return df


def tratar_coluna_valor(df: pd.DataFrame, col: str = "Valor") -> pd.DataFrame:
    """
    Trata a coluna Valor: converte 'NULL' para NaN e tenta parsing numérico.
    Registros com vírgula decimal (ex: '43,79') são convertidos corretamente.

    Controle de Alterações
    ----------------------
    Campo    : Valor
    Problema : String 'NULL' e vírgula como separador decimal
    Tratamento: Substituir 'NULL'→NaN, vírgula→ponto, converter para float
    Justificativa: Permitir uso como feature numérica em modelos
    """
    antes_nulos = df[col].eq("NULL").sum()
    df[col] = df[col].replace("NULL", np.nan)
    df[col] = df[col].str.replace(",", ".", regex=False)
    df[col] = pd.to_numeric(df[col], errors="coerce")
    depois_nulos = df[col].isna().sum()

    print(f"  🔧 Coluna 'Valor' tratada:")
    print(f"     'NULL' convertidos para NaN : {antes_nulos:,}")
    print(f"     Total NaN após conversão    : {depois_nulos:,} ({depois_nulos/len(df)*100:.2f}%)")
    return df


def extrair_features_temporais(df: pd.DataFrame, col_ts: str = "Data_Evento") -> pd.DataFrame:
    """
    Extrai features temporais do timestamp do evento.

    Features criadas:
    - hora_dia       : 0–23
    - dia_semana     : 0=segunda ... 6=domingo
    - dia_mes        : 1–31
    - mes            : 1–12
    - turno          : 'dia' (06h–18h) ou 'noite' (18h–06h)
    - is_fim_semana  : 1 se sábado ou domingo
    """
    df[col_ts] = pd.to_datetime(df[col_ts])

    df["hora_dia"]      = df[col_ts].dt.hour
    df["dia_semana"]    = df[col_ts].dt.dayofweek      # 0=seg, 6=dom
    df["dia_mes"]       = df[col_ts].dt.day
    df["mes"]           = df[col_ts].dt.month
    df["turno"]         = df["hora_dia"].apply(lambda h: "dia" if 6 <= h < 18 else "noite")
    df["is_fim_semana"] = (df["dia_semana"] >= 5).astype(int)

    print(f"  ✅ Features temporais extraídas: hora_dia, dia_semana, dia_mes, mes, turno, is_fim_semana")
    return df


def calcular_duracao_ciclo_apontamentos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula a duração de cada ciclo de apontamento em minutos.

    Controle de Alterações
    ----------------------
    Campo    : duracao_min (nova coluna)
    Fórmula  : (Fim - Inicio).total_seconds() / 60
    Ciclos negativos ou zero: {n} registros — investigar
    """
    df["duracao_min"] = (
        pd.to_datetime(df["Fim"]) - pd.to_datetime(df["Inicio"])
    ).dt.total_seconds() / 60

    negativos = (df["duracao_min"] <= 0).sum()
    if negativos > 0:
        print(f"  ⚠️  Ciclos com duração <= 0: {negativos} — verificar manualmente")
    else:
        print(f"  ✅ Nenhum ciclo com duração negativa ou zero encontrado.")
    return df


# ─── RELATÓRIO DE QUALIDADE ───────────────────────────────────────────────────

def relatorio_qualidade(df: pd.DataFrame, nome: str = "DataFrame") -> pd.DataFrame:
    """
    Gera relatório de qualidade do DataFrame no padrão do Estudo Guiado (CM 2.1).

    Retorna DataFrame com: Feature, Tipo, % Nulos, Min, Max, Média, Mediana, Desvio Padrão
    """
    print(f"\n{'='*60}")
    print(f"  RELATÓRIO DE QUALIDADE — {nome}")
    print(f"{'='*60}")
    print(f"  Shape         : {df.shape[0]:,} linhas × {df.shape[1]} colunas")
    print(f"  Duplicatas    : {df.duplicated().sum():,}")
    print(f"  Período       : {df.index.min() if isinstance(df.index, pd.DatetimeIndex) else 'ver coluna de data'}")

    registros = []
    for col in df.columns:
        pct_nulos = df[col].isna().sum() / len(df) * 100
        tipo = str(df[col].dtype)

        if pd.api.types.is_numeric_dtype(df[col]):
            registros.append({
                "Feature"      : col,
                "Tipo"         : tipo,
                "% Nulos"      : f"{pct_nulos:.2f}%",
                "Min"          : round(df[col].min(), 4),
                "Max"          : round(df[col].max(), 4),
                "Média"        : round(df[col].mean(), 4),
                "Mediana"      : round(df[col].median(), 4),
                "Desvio Padrão": round(df[col].std(), 4),
            })
        else:
            n_unicos = df[col].nunique()
            registros.append({
                "Feature"      : col,
                "Tipo"         : tipo,
                "% Nulos"      : f"{pct_nulos:.2f}%",
                "Min"          : f"{n_unicos} únicos",
                "Max"          : "—",
                "Média"        : "—",
                "Mediana"      : "—",
                "Desvio Padrão": "—",
            })

    relatorio = pd.DataFrame(registros)
    print(f"\n{relatorio.to_string(index=False)}")
    return relatorio


def checar_balanceamento(df: pd.DataFrame, col_target: str = "Is_Dont_Go") -> None:
    """
    Exibe o balanceamento da variável alvo e alerta sobre desbalanceamento extremo.
    """
    contagem = df[col_target].value_counts()
    pct      = df[col_target].value_counts(normalize=True) * 100

    print(f"\n{'='*60}")
    print(f"  BALANCEAMENTO DA VARIÁVEL ALVO — {col_target}")
    print(f"{'='*60}")
    for val in contagem.index:
        print(f"  {val} : {contagem[val]:>12,} registros ({pct[val]:.4f}%)")

    ratio = contagem.max() / contagem.min()
    print(f"\n  Ratio desbalanceamento: {ratio:,.0f}:1")
    if ratio > 100:
        print("  🚨 DESBALANCEAMENTO EXTREMO — usar class_weight='balanced' ou SMOTE")
        print("     NÃO use Accuracy como métrica principal. Use Recall, F1 e AUC-PR.")


# ─── PIPELINE COMPLETO ────────────────────────────────────────────────────────

def pipeline_limpeza_telemetria(arquivos: list, salvar_em: str = None) -> pd.DataFrame:
    """
    Pipeline completo de limpeza da telemetria.
    Executa todas as etapas em sequência e opcionalmente salva o resultado.

    Uso:
        from src.limpeza import pipeline_limpeza_telemetria
        from src.config import TELEMETRIA_FILES, TELEMETRIA_LIMPA

        df = pipeline_limpeza_telemetria(TELEMETRIA_FILES, salvar_em=TELEMETRIA_LIMPA)
    """
    print("\n🚀 INICIANDO PIPELINE DE LIMPEZA — TELEMETRIA")
    print("="*60)

    print("\n[1/5] Carregando arquivos...")
    df = carregar_telemetria_completa(arquivos)

    print("\n[2/5] Normalizando Criticidade...")
    df = normalizar_criticidade(df)

    print("\n[3/5] Removendo colunas inúteis...")
    df = remover_colunas_inuteis(df)

    print("\n[4/5] Tratando coluna Valor...")
    df = tratar_coluna_valor(df)

    print("\n[5/5] Extraindo features temporais...")
    df = extrair_features_temporais(df)

    print("\n📊 Checando balanceamento do target...")
    checar_balanceamento(df)

    print("\n📋 Relatório de qualidade final...")
    relatorio_qualidade(df, nome="Telemetria Limpa")

    if salvar_em:
        salvar_em = Path(salvar_em)
        salvar_em.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(salvar_em, index=False)
        print(f"\n💾 Salvo em: {salvar_em}")

    print("\n✅ Pipeline de limpeza concluído!")
    return df


if __name__ == "__main__":
    print("limpeza.py — funções disponíveis:")
    print("  carregar_telemetria_completa()")
    print("  normalizar_criticidade()")
    print("  remover_colunas_inuteis()")
    print("  tratar_coluna_valor()")
    print("  extrair_features_temporais()")
    print("  calcular_duracao_ciclo_apontamentos()")
    print("  relatorio_qualidade()")
    print("  checar_balanceamento()")
    print("  pipeline_limpeza_telemetria()  ← roda tudo de uma vez")
