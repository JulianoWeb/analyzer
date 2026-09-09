# Site Analyzer 🔎

Ferramenta simples feita em Python para analisar um domínio.

## Funcionalidades

* Busca subdomínios via DNS
* Busca subdomínios via API
* Verifica algumas portas
* Salva os resultados em um arquivo `.txt`

## Instalação

```bash
pip install requests dnspython colorama
```

## Como usar

```bash
python main.py
```

Digite o domínio:

```text
example.com
```

Os resultados serão salvos em:

```text
resultado_example.com.txt
```

## Tecnologias

* Python
* DNS
* Requests
* Socket
* Colorama
