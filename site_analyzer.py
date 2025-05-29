import requests
import dns.resolver
import socket
from colorama import init, Fore

init(autoreset=True)

# Dicionário básico de subdomínios para testar
SUBDOMINIOS = ["www", "mail", "ftp", "api", "blog", "test", "dev", "shop"]

def buscar_subdominios_dns(dominio):
    encontrados = []
    print(Fore.CYAN + "\n🔎 Buscando subdomínios via DNS...\n")
    for sub in SUBDOMINIOS:
        alvo = f"{sub}.{dominio}"
        try:
            dns.resolver.resolve(alvo, 'A')
            print(Fore.GREEN + f"[✔] {alvo} encontrado!")
            encontrados.append(alvo)
        except:
            print(Fore.RED + f"[x] {alvo} não existe.")
    return encontrados

def buscar_subdominios_api(dominio):
    print(Fore.CYAN + "\n🌐 Buscando subdomínios via API hackertarget.com...\n")
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={dominio}"
        resposta = requests.get(url)
        if "error" in resposta.text.lower():
            print(Fore.RED + "Erro: API limitou ou domínio inválido.")
            return []
        linhas = resposta.text.strip().split("\n")
        return [linha.split(",")[0] for linha in linhas]
    except Exception as e:
        print(Fore.RED + f"Erro: {e}")
        return []

def scanner_portas(dominio, portas=[21,22,23,25,53,80,110,143,443,3306,8080]):
    print(Fore.CYAN + "\n🔒 Escaneando portas abertas...\n")
    abertos = []
    for porta in portas:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            resultado = sock.connect_ex((dominio, porta))
            if resultado == 0:
                print(Fore.GREEN + f"[✔] Porta {porta} aberta!")
                abertos.append(porta)
            else:
                print(Fore.RED + f"[x] Porta {porta} fechada.")
            sock.close()
        except:
            print(Fore.RED + f"[!] Não foi possível escanear a porta {porta}.")
    return abertos

def salvar_resultados(nome_arquivo, subdominios, portas):
    with open(nome_arquivo, "w") as f:
        f.write("=== Subdomínios Encontrados ===\n")
        for s in subdominios:
            f.write(f"{s}\n")
        f.write("\n=== Portas Abertas ===\n")
        for p in portas:
            f.write(f"Porta {p}\n")
    print(Fore.YELLOW + f"\n📁 Resultados salvos em: {nome_arquivo}")

def main():
    print(Fore.MAGENTA + "\n=== Site Analyzer CLI ===")
    dominio = input(Fore.WHITE + "Digite o domínio (ex: example.com): ")

    # Buscar subdomínios
    sub_dns = buscar_subdominios_dns(dominio)
    sub_api = buscar_subdominios_api(dominio)
    sub_total = list(set(sub_dns + sub_api))

    # Scanner de portas
    portas_abertas = scanner_portas(dominio)

    # Salvar resultados
    nome_arquivo = f"resultado_{dominio}.txt"
    salvar_resultados(nome_arquivo, sub_total, portas_abertas)

    print(Fore.CYAN + "\n🔍 Fim da análise. Até mais!")

if __name__ == "__main__":
    main()
