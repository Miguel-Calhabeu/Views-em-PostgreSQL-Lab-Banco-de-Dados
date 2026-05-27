# Guia de Uso e Gerenciamento do Banco de Dados Isolado (PostgreSQL 16)

> **Disciplina:** SCC-541 – Laboratório de Bases de Dados — ICMC/USP São Carlos  
> **Ambiente:** Local Isolado (Porta 5433)  

Este documento descreve as instruções de controle, conexão e administração para a instância local e independente do PostgreSQL 16 configurada na pasta do projeto. Este ambiente foi projetado para rodar de forma totalmente isolada de outras instâncias instaladas no sistema operacional, utilizando a porta **5433** e armazenando os dados na pasta local `db_data/`.

---

## 1. Parâmetros de Conexão

Para se conectar à base de dados integrada da disciplina (Fórmula 1 + Cidades + Aeroportos), utilize as seguintes credenciais e configurações:

| Parâmetro | Valor | Observação |
| :--- | :--- | :--- |
| **Host** | `localhost` ou `127.0.0.1` | Execução local na própria máquina |
| **Porta** | `5433` | Porta dedicada para evitar conflitos com instâncias na porta padrão 5432 |
| **Banco de Dados (Database)** | `labbd` | Banco exclusivo de laboratório |
| **Usuário (Username)** | `labbd` | Administrador da base |
| **Senha (Password)** | *(Sem senha)* | Autenticação local em modo confiável (`trust`) |

---

## 2. Comandos de Gerenciamento do Servidor (CLI)

Os utilitários do PostgreSQL instalados via Homebrew no macOS são utilizados para controlar a inicialização e o desligamento do servidor. Os comandos a seguir devem ser executados dentro da raiz da pasta operacional:

```bash
cd /Users/user/Faculdade/Views-em-PostgreSQL-Lab-Banco-de-Dados
```

### 2.1. Iniciar o Banco de Dados
Caso o servidor seja parado ou após reiniciar o computador, suba a instância com o seguinte comando:
```bash
/opt/homebrew/opt/postgresql@16/bin/pg_ctl -D db_data -l db_data/postgresql.log -o "-p 5433" start
```
* **O que faz:** Inicializa o processo do PostgreSQL em segundo plano, direciona os logs para `db_data/postgresql.log` e ativa a escuta de rede na porta `5433`.

### 2.2. Verificar Status do Servidor
Verifique se a instância está ativa e respondendo a conexões:
```bash
/opt/homebrew/opt/postgresql@16/bin/pg_isready -p 5433
```
* **Retorno esperado:** `/tmp:5433 - accepting connections`

### 2.3. Parar o Banco de Dados
Para encerrar a instância com segurança e persistir todos os buffers pendentes em disco:
```bash
/opt/homebrew/opt/postgresql@16/bin/pg_ctl -D db_data stop
```
* **O que faz:** Envia um sinal de encerramento controlado (*SIGTERM*) para o daemon do PostgreSQL, desliga as escutas de rede e encerra os processos filhos.

---

## 3. Como se Conectar ao Banco de Dados

### 3.1. Via Terminal Interativo (psql CLI)
O terminal interativo é ideal para execuções rápidas e consultas diretas:
```bash
/opt/homebrew/opt/postgresql@16/bin/psql -p 5433 -U labbd -d labbd
```

### 3.2. Via Ferramentas Visuais (DBeaver / pgAdmin / DataGrip)
Para conectar usando ferramentas gráficas de gerenciamento de dados:
1. Abra sua ferramenta (ex: DBeaver).
2. Crie uma nova conexão do tipo **PostgreSQL**.
3. Na guia de configurações de rede/conexão, preencha:
   * **Host:** `localhost`
   * **Port:** `5433`
   * **Database:** `labbd`
   * **Username:** `labbd`
   * **Password:** Deixe em branco (se a ferramenta exigir, digite qualquer valor ou desmarque a obrigatoriedade de senha).
4. Clique em **Test Connection** e depois em **Finish**.

---

## 4. Execução de Scripts da Disciplina

### 4.1. Rodando o Script do Trabalho T4 (Views)
Para rodar e testar o script de views da entrega anterior:
```bash
/opt/homebrew/opt/postgresql@16/bin/psql -p 5433 -U labbd -d labbd -f t4_views.sql
```

### 4.2. Rodando o Script do Trabalho T5 (Índices)
Para rodar a bateria de testes de índices, recriá-los e mensurar a performance:
```bash
/opt/homebrew/opt/postgresql@16/bin/psql -p 5433 -U labbd -d labbd -f t5_indices.sql
```

---

## 5. Resolução de Problemas Comuns

### 5.1. Erro: "Port 5433 already in use"
Se o servidor acusar que a porta já está ocupada, localize o processo que a está utilizando e encerre-o:
```bash
lsof -i :5433
```
Identifique o `PID` do processo PostgreSQL e encerre-o:
```bash
kill -9 <PID>
```

### 5.2. Erro de inicialização após queda de energia ("postmaster.pid")
Se o computador desligar incorretamente enquanto o PostgreSQL estiver rodando, o servidor pode recusar a iniciar acusando a presença de um arquivo de trava (*lockfile*).
* **Solução:** Delete o arquivo de lock residual e reinicie o banco:
  ```bash
  rm -f db_data/postmaster.pid
  /opt/homebrew/opt/postgresql@16/bin/pg_ctl -D db_data -l db_data/postgresql.log -o "-p 5433" start
  ```
