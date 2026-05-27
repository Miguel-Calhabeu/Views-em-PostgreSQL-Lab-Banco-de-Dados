#!/bin/bash

# ============================================================
# SETUP ISOLADO POSTGRESQL LOCAL E VALIDAÇÃO DO TRABALHO T5
# ============================================================

set -e

# 1. Definições de caminhos e parâmetros
BASE_DIR="/Users/user/Faculdade/Views-em-PostgreSQL-Lab-Banco-de-Dados"
DB_DATA="$BASE_DIR/db_data"
DB_PORT="5433" # Porta isolada para evitar conflitos
DB_USER="labbd"
DB_DB="labbd"

echo "============================================================"
echo "🚀 Iniciando Setup Isolado do PostgreSQL Local"
echo "============================================================"

# 2. Localizar binários do PostgreSQL do Homebrew
echo "🔍 Buscando binários do PostgreSQL 16..."
PG_PATH=""
if [ -d "/opt/homebrew/opt/postgresql@16/bin" ]; then
    PG_PATH="/opt/homebrew/opt/postgresql@16/bin"
elif [ -d "/usr/local/opt/postgresql@16/bin" ]; then
    PG_PATH="/usr/local/opt/postgresql@16/bin"
elif command -v initdb &> /dev/null; then
    PG_PATH=$(dirname "$(command -v initdb)")
fi

if [ -z "$PG_PATH" ]; then
    echo "❌ Erro: Não foi possível localizar os utilitários do PostgreSQL 16."
    exit 1
fi

echo "✅ PostgreSQL localizado em: $PG_PATH"
export PATH="$PG_PATH:$PATH"

# 3. Inicializar diretório de dados (se não existir)
if [ ! -d "$DB_DATA" ]; then
    echo "📁 Criando diretório de dados isolado em: $DB_DATA"
    mkdir -p "$DB_DATA"
    echo "⚙️ Inicializando base de dados com initdb..."
    initdb -D "$DB_DATA" -U "$DB_USER" --auth=trust
else
    echo "📁 Diretório de dados já existente em: $DB_DATA"
fi

# 4. Iniciar o servidor PostgreSQL em background
echo "⚡ Iniciando servidor PostgreSQL na porta $DB_PORT..."
# Verifica se já está rodando
if pg_isready -p "$DB_PORT" &> /dev/null; then
    echo "ℹ️ Servidor PostgreSQL já está rodando na porta $DB_PORT."
else
    pg_ctl -D "$DB_DATA" -l "$DB_DATA/postgresql.log" -o "-p $DB_PORT" start
    sleep 3
fi

# 5. Aguardar conexão estar pronta
echo "⏳ Aguardando banco aceitar conexões..."
until pg_isready -p "$DB_PORT" &> /dev/null; do
    sleep 1
done
echo "✅ Servidor PostgreSQL está online!"

# 6. Criar banco de dados se não existir
echo "🔨 Verificando banco de dados '$DB_DB'..."
if psql -p "$DB_PORT" -U "$DB_USER" -d template1 -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_DB'" | grep -q 1; then
    echo "ℹ️ Banco de dados '$DB_DB' já existe."
else
    echo "🔨 Criando banco de dados '$DB_DB'..."
    createdb -p "$DB_PORT" -U "$DB_USER" "$DB_DB"
fi

# 7. Carregar o Schema
echo "📝 Criando tabelas da disciplina (schema.sql)..."
psql -p "$DB_PORT" -U "$DB_USER" -d "$DB_DB" -f "$BASE_DIR/docker-labbd/schema.sql"

# 8. Ajustar caminhos de cópia e carregar dados
echo "⚙️ Adaptando caminhos de arquivos para carga local..."
CARGA_ORIGINAL="$BASE_DIR/docker-labbd/carga_docker.sql"
CARGA_LOCAL="$BASE_DIR/docker-labbd/carga_local.sql"

# Substitui o caminho /dados/ do container docker pelo caminho absoluto dos CSVs locais
sed "s|'/dados/|'$BASE_DIR/docker-labbd/dados/|g" "$CARGA_ORIGINAL" > "$CARGA_LOCAL"

echo "📥 Carregando dados da Fórmula 1 + Dados Geográficos (carga_local.sql)..."
echo "⚠️  Nota: A carga de cidades e aeroportos pode levar até 2 minutos. Aguarde..."
psql -p "$DB_PORT" -U "$DB_USER" -d "$DB_DB" -f "$CARGA_LOCAL"

echo "✅ Carga concluída com sucesso!"

# 9. Validar se a carga funcionou
echo "📊 Estatísticas da base carregada localmente:"
psql -p "$DB_PORT" -U "$DB_USER" -d "$DB_DB" -c "
SELECT 'airports' AS tabela, COUNT(*) AS contagem FROM airports UNION ALL
SELECT 'cities' AS tabela, COUNT(*) AS contagem FROM cities UNION ALL
SELECT 'countries' AS tabela, COUNT(*) AS contagem FROM countries UNION ALL
SELECT 'circuits' AS tabela, COUNT(*) AS contagem FROM circuits UNION ALL
SELECT 'drivers' AS tabela, COUNT(*) AS contagem FROM drivers UNION ALL
SELECT 'races' AS tabela, COUNT(*) AS contagem FROM races;
"

# 10. Validar a Task 5 (Script de Índices)
echo "🔬 Executando validação prática da Task 5 (t5_indices.sql)..."
psql -p "$DB_PORT" -U "$DB_USER" -d "$DB_DB" -f "$BASE_DIR/t5_indices.sql"

echo "============================================================"
echo "🎉 Setup isolado e Validação da Task 5 concluídos com sucesso!"
echo "============================================================"
