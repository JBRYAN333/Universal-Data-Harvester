# Universal Data Harvester

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)

**Universal Data Harvester** - Sistema modular de coleta, processamento e exportação de dados de múltiplas fontes com arquitetura extensível baseada em plugins.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Características Principais](#características-principais)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Módulos Disponíveis](#módulos-disponíveis)
- [API](#api)
- [Exemplos](#exemplos)
- [Desenvolvimento](#desenvolvimento)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## 🎯 Visão Geral

O **Universal Data Harvester** é uma plataforma de código aberto projetada para simplificar e padronizar a coleta de dados de fontes heterogêneas. Com arquitetura baseada em plugins, o sistema permite coletar, transformar e exportar dados de APIs REST, bancos de dados, arquivos locais, web scraping e streams em tempo real.

### Casos de Uso

- **Monitoramento de Preços**: Coleta automática de preços de e-commerces
- **Análise de Redes Sociais**: Harvesting de dados de plataformas sociais
- **Backup de Dados**: Exportação automatizada de bancos de dados
- **Pesquisa Acadêmica**: Coleta de dados para estudos científicos
- **Business Intelligence**: Agregação de métricas de múltiplas fontes
- **IoT Data Collection**: Processamento de streams de dispositivos IoT

## ✨ Características Principais

### 🔌 **Extensibilidade Modular**
- Sistema baseado em plugins para fontes, transformações e destinos
- API clara para desenvolvimento de novos módulos
- Hot-reload de módulos sem reinicialização

### ⚡ **Performance Otimizada**
- Processamento assíncrono com asyncio
- Cache inteligente com TTL configurável
- Rate limiting e retry automático
- Suporte a processamento em lote e streaming

### 🔒 **Segurança e Confiabilidade**
- Autenticação OAuth2 para APIs protegidas
- Criptografia de credenciais
- Logging detalhado com diferentes níveis
- Sistema de health checks e monitoramento

### 📊 **Processamento Avançado**
- Pipeline de transformações encadeáveis
- Validação de schema com JSON Schema
- Normalização e deduplicação de dados
- Suporte a joins e agregações

### 🚀 **Deploy Flexível**
- Containerização com Docker
- Orquestração com Kubernetes
- Deploy serverless (AWS Lambda, Google Cloud Functions)
- Execução local ou em cloud

## 🏗️ Arquitetura

```
universal-data-harvester/
├── core/                    # Núcleo do sistema
│   ├── engine.py           # Motor de execução
│   ├── pipeline.py         # Gerenciador de pipelines
│   ├── scheduler.py        # Agendador de tarefas
│   └── cache.py           # Sistema de cache
├── plugins/                # Módulos extensíveis
│   ├── sources/           # Fontes de dados
│   │   ├── api.py        # APIs REST/GraphQL
│   │   ├── database.py   # Bancos de dados
│   │   ├── file.py       # Arquivos locais
│   │   └── web.py        # Web scraping
│   ├── transformers/      # Transformações
│   │   ├── filter.py     # Filtragem
│   │   ├── mapper.py     # Mapeamento
│   │   ├── aggregator.py # Agregação
│   │   └── validator.py  # Validação
│   └── destinations/      # Destinos
│       ├── database.py   # Bancos de dados
│       ├── file.py       # Arquivos
│       ├── api.py        # APIs externas
│       └── message_queue.py # Filas de mensagens
├── config/                # Configuração
│   ├── schemas/          # JSON Schemas
│   └── templates/        # Templates de pipeline
├── utils/                # Utilitários
│   ├── auth.py          # Autenticação
│   ├── logger.py        # Logging
│   └── metrics.py       # Métricas
└── tests/               # Testes
```

### Fluxo de Dados

```mermaid
graph LR
    A[Fonte de Dados] --> B[Adapter]
    B --> C[Pipeline]
    C --> D[Transformação 1]
    D --> E[Transformação 2]
    E --> F[Validação]
    F --> G[Cache]
    G --> H[Destino]
```

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)

### Instalação via pip

```bash
# Instalar versão estável
pip install universal-data-harvester

# Instalar versão de desenvolvimento
pip install git+https://github.com/JBRYAN333/Universal-Data-Harvester.git
```

### Instalação via Docker

```bash
# Pull da imagem Docker
docker pull jbryan333/universal-data-harvester:latest

# Executar container
docker run -d \
  --name data-harvester \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  jbryan333/universal-data-harvester:latest
```

### Instalação Manual

```bash
# Clonar repositório
git clone https://github.com/JBRYAN333/Universal-Data-Harvester.git
cd Universal-Data-Harvester

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Para desenvolvimento
```

## ⚙️ Configuração

### Arquivo de Configuração Principal

Crie um arquivo `config.yaml` na raiz do projeto:

```yaml
# config.yaml
version: "1.0"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/harvester.log"

cache:
  enabled: true
  ttl: 3600  # segundos
  backend: "redis"  # ou "memory", "file"
  redis_url: "redis://localhost:6379/0"

scheduler:
  enabled: true
  timezone: "America/Sao_Paulo"
  jobs:
    - name: "daily_price_check"
      cron: "0 9 * * *"  # 9AM daily
      pipeline: "price_monitoring"

plugins:
  auto_discover: true
  directories:
    - "./plugins"
    - "~/.harvester/plugins"

security:
  encryption_key: "${ENCRYPTION_KEY}"  # Variável de ambiente
  secrets_backend: "env"  # ou "vault", "aws_secrets"
```

### Variáveis de Ambiente

```bash
# .env file
HARVESTER_LOG_LEVEL=INFO
HARVESTER_CACHE_BACKEND=redis
REDIS_URL=redis://localhost:6379
ENCRYPTION_KEY=your-secure-encryption-key
DATABASE_URL=postgresql://user:pass@localhost:5432/harvester
```

## 🚀 Uso

### Interface de Linha de Comando (CLI)

```bash
# Mostrar ajuda
harvester --help

# Executar pipeline específico
harvester run --pipeline price_monitoring

# Executar com configuração customizada
harvester run --config custom_config.yaml --pipeline social_media

# Listar pipelines disponíveis
harvester list --pipelines

# Listar plugins carregados
harvester list --plugins

# Verificar status do sistema
harvester status

# Monitorar execução em tempo real
harvester monitor --pipeline iot_stream
```

### API REST

```python
import requests

# Iniciar pipeline via API
response = requests.post(
    "http://localhost:8000/api/v1/pipelines/run",
    json={
        "pipeline": "price_monitoring",
        "parameters": {
            "urls": ["https://api.example.com/prices"],
            "interval": 300
        }
    },
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

# Verificar status
status = requests.get("http://localhost:8000/api/v1/status")
```

### Programático (Python)

```python
from harvester import HarvesterEngine
from harvester.plugins import APISource, CSVDestination, JSONTransformer

# Configurar engine
engine = HarvesterEngine(config_path="config.yaml")

# Criar pipeline programático
pipeline = engine.create_pipeline(
    name="custom_pipeline",
    description="Pipeline personalizado para coleta de dados"
)

# Adicionar fonte
pipeline.add_source(
    APISource(
        endpoint="https://api.example.com/data",
        auth_type="oauth2",
        params={"limit": 100}
    )
)

# Adicionar transformação
pipeline.add_transformer(
    JSONTransformer(
        mapping={
            "id": "$.id",
            "name": "$.attributes.name",
            "price": "$.attributes.price"
        }
    )
)

# Adicionar destino
pipeline.add_destination(
    CSVDestination(
        file_path="output/data.csv",
        columns=["id", "name", "price", "timestamp"]
    )
)

# Executar pipeline
results = pipeline.run()
print(f"Dados coletados: {len(results)} registros")
```

## 🔌 Módulos Disponíveis

### Fontes de Dados (Sources)

#### API Source
```yaml
- type: api
  name: rest_api
  config:
    endpoint: "https://api.example.com/v1/data"
    method: GET
    auth:
      type: bearer_token
      token: "${API_TOKEN}"
    headers:
      User-Agent: "UniversalDataHarvester/1.0"
    params:
      limit: 100
      offset: 0
```

#### Database Source
```yaml
- type: database
  name: postgres_source
  config:
    connection_string: "${DATABASE_URL}"
    query: "SELECT * FROM products WHERE updated_at > :last_run"
    parameters:
      last_run: "2024-01-01"
```

#### File Source
```yaml
- type: file
  name: csv_reader
  config:
    path: "data/input/products.csv"
    format: csv
    delimiter: ","
    encoding: utf-8
```

#### Web Scraping Source
```yaml
- type: web
  name: website_scraper
  config:
    url: "https://example.com/products"
    selector: ".product-item"
    pagination:
      enabled: true
      next_button: ".next-page"
    delay: 2  # segundos entre requests
```

### Transformadores (Transformers)

#### Filter Transformer
```yaml
- type: filter
  name: price_filter
  config:
    condition: "item.price > 0 and item.price < 1000"
```

#### Map Transformer
```yaml
- type: map
  name: field_mapper
  config:
    mapping:
      product_id: "id"
      product_name: "name"
      product_price: "price"
      currency: "USD"
```

#### Aggregate Transformer
```yaml
- type: aggregate
  name: daily_stats
  config:
    group_by: ["date"]
    aggregations:
      total_sales: {"field": "price", "operation": "sum"}
      avg_price: {"field": "price", "operation": "avg"}
      count: {"field": "id", "operation": "count"}
```

#### Validate Transformer
```yaml
- type: validate
  name: schema_validator
  config:
    schema:
      type: object
      required: ["id", "name", "price"]
      properties:
        id:
          type: string
          pattern: "^[A-Z0-9]{8}$"
        name:
          type: string
          minLength: 1
          maxLength: 100
        price:
          type: number
          minimum: 0
```

### Destinos (Destinations)

#### Database Destination
```yaml
- type: database
  name: postgres_destination
  config:
    connection_string: "${DATABASE_URL}"
    table: "harvested_data"
    mode: upsert  # insert, update, upsert, truncate
    conflict_columns: ["id"]
```

#### File Destination
```yaml
- type: file
  name: json_exporter
  config:
    path: "data/output/products.json"
    format: json
    indent: 2
    mode: append  # overwrite, append
```

#### API Destination
```yaml
- type: api
  name: webhook_sender
  config:
    endpoint: "https://webhook.example.com/data"
    method: POST
    batch_size: 100
    headers:
      Content-Type: "application/json"
```

#### Message Queue Destination
```yaml
- type: message_queue
  name: kafka_producer
  config:
    bootstrap_servers: "localhost:9092"
    topic: "harvested_data"
    key_field: "id"
```

## 📚 Exemplos

### Exemplo 1: Monitoramento de Preços de E-commerce

```yaml
# pipelines/price_monitoring.yaml
name: price_monitoring
description: "Monitoramento diário de preços em múltiplos e-commerces"
schedule: "0 9 * * *"  # 9AM daily

sources:
  - type: web
    name: amazon_prices
    config:
      url: "https://www.amazon.com/dp/{product_id}"
      selectors:
        price: "#priceblock_ourprice"
        title: "#productTitle"
      products:
        - product_id: "B08N5WRWNW"
        - product_id: "B08N5WV27P"

transformers:
  - type: map
    name: normalize_prices
    config:
      mapping:
        source: "amazon"
        product_id: "product_id"
        price: "float(price.replace('$', ''))"
        currency: "USD"
        timestamp: "datetime.now().isoformat()"

  - type: validate
    name: validate_data
    config:
      schema:
        type: object
        required: ["source", "product_id", "price", "currency"]
        properties:
          price:
            type: number
            minimum: 0

destinations:
  - type: database
    name: postgres_store
    config:
      table: "price_history"
      mode: append

  - type: file
    name: csv_backup
    config:
      path: "data/prices/amazon_{date}.csv"
      format: csv
```

### Exemplo 2: Coleta de Dados de Redes Sociais

```python
# social_media_pipeline.py
from harvester import HarvesterEngine
from harvester.plugins import (
    APISource, 
    JSONTransformer,
    FilterTransformer,
    DatabaseDestination
)

engine = HarvesterEngine()

# Pipeline para Twitter/X
twitter_pipeline = engine.create_pipeline("twitter_collection")

twitter_pipeline.add_source(
    APISource(
        endpoint="https://api.twitter.com/2/tweets/search/recent",
        auth_type="bearer",
        params={
            "query": "data science",
            "max_results": 100,
            "tweet.fields": "created_at,public_metrics"
        }
    )
)

twitter_pipeline.add_transformer(
    JSONTransformer(
        mapping={
            "tweet_id": "$.id",
            "text": "$.text",
            "author_id": "$.author_id",
            "created_at": "$.created_at",
            "retweets": "$.public_metrics.retweet_count",
            "likes": "$.public_metrics.like_count"
        }
    )
)

twitter_pipeline.add_transformer(
    FilterTransformer(
        condition="item.retweets > 10 or item.likes > 50"
    )
)

twitter_pipeline.add_destination(
    DatabaseDestination(
        table="tweets",
        conflict_columns=["tweet_id"]
    )
)

# Executar pipeline
engine.run_pipeline("twitter_collection")
```

### Exemplo 3: Pipeline em Tempo Real para IoT

```yaml
# pipelines/iot_stream.yaml
name: iot_stream_processing
description: "Processamento em tempo real de dados de sensores IoT"
mode: streaming  # vs batch

sources:
  - type: message_queue
    name: mqtt_subscriber
    config:
      broker: "tcp://iot-broker:1883"
      topic: "sensors/+/data"
      qos: 1

transformers:
  - type: map
    name: parse_sensor_data
    config:
      mapping:
        device_id: "topic.split('/')[1]"
        timestamp: "datetime.fromtimestamp(payload.timestamp)"
        temperature: "float(payload.temperature)"
        humidity: "float(payload.humidity)"
        battery: "int(payload.battery_level)"

  - type: validate
    name: validate_sensor_readings
    config:
      schema:
        type: object
        required: ["device_id", "timestamp", "temperature"]
        properties:
          temperature:
            type: number
            minimum: -40
            maximum: 85

  - type: aggregate
    name: hourly_aggregates
    config:
      window: "1 hour"
      aggregations:
        avg_temperature: {"field": "temperature", "operation": "avg"}
        max_temperature: {"field": "temperature", "operation": "max"}
        min_temperature: {"field": "temperature", "operation": "min"}
        reading_count: {"field": "device_id", "operation": "count"}

destinations:
  - type: database
    name: timescale_db
    config:
      table: "sensor_readings"
      mode: append

  - type: api
    name: alert_webhook
    config:
      endpoint: "https://alerts.example.com/webhook"
      condition: "item.temperature > 30 or item.temperature < 10"
```

## 🛠️ Desenvolvimento

### Estrutura do Plugin

```python
# plugins/sources/custom_source.py
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from harvester.core import BaseSource, DataRecord

@dataclass
class CustomSourceConfig:
    """Configuração para CustomSource."""
    api_key: str
    endpoint: str
    timeout: int = 30

class CustomSource(BaseSource):
    """Fonte de dados personalizada."""
    
    name = "custom_source"
    version = "1.0.0"
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.config = CustomSourceConfig(**config)
        
    async def connect(self):
        """Conectar à fonte de dados."""
        self.logger.info(f"Conectando a {self.config.endpoint}")
        # Implementar conexão
        
    async def fetch(self, params: Optional[Dict] = None) -> List[DataRecord]:
        """Buscar dados da fonte."""
        try:
            # Implementar lógica de fetch
            data = await self._make_request(params)
            records = self._parse_response(data)
            return records
        except Exception as e:
            self.logger.error(f"Erro ao buscar dados: {e}")
            raise
            
    async def disconnect(self):
        """Desconectar da fonte."""
        self.logger.info("Desconectando da fonte")
        # Implementar desconexão
        
    def get_metrics(self) -> Dict[str, Any]:
        """Retornar métricas do source."""
        return {
            "requests_made": self._request_count,
            "bytes_received": self._bytes_received,
            "success_rate": self._success_rate
        }
```

### Testes

```python
# tests/test_custom_source.py
import pytest
from unittest.mock import AsyncMock, patch
from plugins.sources.custom_source import CustomSource

@pytest.mark.asyncio
async def test_custom_source_fetch():
    """Testar fetch do CustomSource."""
    config = {
        "api_key": "test_key",
        "endpoint": "https://api.example.com/test"
    }
    
    source = CustomSource(config)
    
    with patch.object(source, '_make_request') as mock_request:
        mock_request.return_value = {"data": [{"id": 1, "name": "Test"}]}
        
        records = await source.fetch()
        
        assert len(records) == 1
        assert records[0].data["id"] == 1
        mock_request.assert_called_once()
```

### Build e Deploy

```bash
# Build do pacote
python setup.py sdist bdist_wheel

# Testar build
twine check dist/*

# Publicar no PyPI
twine upload dist/*

# Build Docker
docker build -t universal-data-harvester:latest .

# Push para Docker Hub
docker tag universal-data-harvester:latest jbryan333/universal-data-harvester:latest
docker push jbryan333/universal-data-harvester:latest
```

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, leia nosso [Guia de Contribuição](CONTRIBUTING.md) antes de submeter pull requests.

### Fluxo de Desenvolvimento

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'Add amazing feature'`)
4. Push para a branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

### Padrões de Código

- Siga [PEP 8](https://www.python.org/dev/peps/pep-0008/) para Python
- Use type hints sempre que possível
- Escreva docstrings para todas as funções públicas
- Mantenha cobertura de testes acima de 80%
- Use [Conventional Commits](https://www.conventionalcommits.org/)

### Checklist para Pull Requests

- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Código segue padrões do projeto
- [ ] Build passa localmente
- [ ] Commits seguem conventional commits

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

- **Autor**: JBRYAN333
- **GitHub**: [https://github.com/JBRYAN333](https://github.com/JBRYAN333)
- **Email**: sufocoprojeto@gmail.com
- **Issues**: [GitHub Issues](https://github.com/JBRYAN333/Universal-Data-Harvester/issues)

## 🙏 Agradecimentos

- A todos os contribuidores que ajudaram a melhorar este projeto
- À comunidade open source por todas as bibliotecas incríveis
- Aos usuários que reportaram bugs e sugeriram melhorias

---

**⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub! ⭐**

[![Star History Chart](https://api.star-history.com/svg?repos=JBRYAN333/Universal-Data-Harvester&type=Date)](https://star-history.com/#JBRYAN333/Universal-Data-Harvester&Date)