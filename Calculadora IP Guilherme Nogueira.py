import time
import os

while True:
    print("=-=-=-=-=-=- CALCULADORA IP -=-=-=-=-=-=")
    IP = input("Digite o IP da rede: ")
    
    try:
        octeto1, octeto2, octeto3, octeto4 = IP.split(".")
    except ValueError:
        print("Endereço IP inválido! Tente de novo...")
        time.sleep(3)
        os.system('cls')
        continue
    
    if len(octeto1) == 0 or len(octeto2) == 0 or len(octeto3) == 0 or len(octeto4) == 0:
        print("Tipo de IP errado, Tente novamente!")
        time.sleep(3)
        os.system('cls')
        continue
    
    valido = True
    for octeto in [octeto1, octeto2, octeto3, octeto4]:
        if not octeto.isdigit() or not (0 <= int(octeto) <= 255):
            valido = False
            break

    if not valido:
        print("Tipo de IP inválido. Tente novamente...")
        time.sleep(3)
        os.system('cls')
        continue
    
    octeto1 = int(octeto1)
    octeto2 = int(octeto2)
    octeto3 = int(octeto3)
    octeto4 = int(octeto4)
    
    escolha = input("O calculo será com CIDR? Se sim, digite S, caso contrário, digite N: ").strip().upper()
    if escolha == "S":
        cidr_mascara = int(input("Escreva o prefixo CIDR (tipo 24 para 255.255.255.0): "))
        
        mascara_binario = "1" * cidr_mascara + "0" * (32 - cidr_mascara)
        
        mascara_sub_rede = (
            int(mascara_binario[0:8], 2), 
            int(mascara_binario[8:16], 2),
            int(mascara_binario[16:24], 2),
            int(mascara_binario[24:32], 2)
        )
        
        ip_binario = "".join([format(int(octeto), '08b') for octeto in [octeto1, octeto2, octeto3, octeto4]])

        rede_binario = ""
        broadcast_binario = ""
        
        for i in range(32):
            if ip_binario[i] == mascara_binario[i]:
                rede_binario += "1"
            else:
                rede_binario += "0"
                
            if mascara_binario[i] == "1":
                broadcast_binario += ip_binario[i]
            else:
                broadcast_binario += "1"

        rede = ".".join([str(int(rede_binario[i:i+8], 2)) for i in range(0, 32, 8)])
        broadcast = ".".join([str(int(broadcast_binario[i:i+8], 2)) for i in range(0, 32, 8)])

        print(f"A rede é: {rede}")
        print(f"O broadcast é: {broadcast}")
        print(f"A máscara de sub-rede é: {mascara_sub_rede[0]}.{mascara_sub_rede[1]}.{mascara_sub_rede[2]}.{mascara_sub_rede[3]}")
        
        if octeto1 >= 1 and octeto1 <= 127:
            classe = 'A'
        elif octeto1 >= 128 and octeto1 <= 191:
            classe = 'B'
        elif octeto1 >= 192 and octeto1 <= 223:
            classe = 'C'
        
        print(f"Classe do IP: {classe}")
        
        if (octeto1 == 10) or (octeto1 == 172 and 16 <= octeto2 <= 31) or (octeto1 == 192 and octeto2 == 168):
            ip_tipo = "privado"
        else:
            ip_tipo = "público"
        
        print(f"Esse IP é {ip_tipo}.")
        
        bits_subrede = 32 - cidr_mascara
        qtd_subredes = 2 ** bits_subrede
        qtd_hosts = (2 ** bits_subrede) - 2 
        
        print(f"Sub-redes possíveis: {qtd_subredes}")
        print(f"Hosts por sub-rede: {qtd_hosts}")
        
    else:
        mascara_rede = input("Digite a máscara de rede: (Ex: 255.255.255.0): ").split(".")

        if len(mascara_rede) != 4:
            print("A máscara está incorreta. tente de novo...")
            time.sleep(3)
            os.system('cls')
            continue
        
        try:
            mascara_rede1 = int(mascara_rede[0])
            mascara_rede2 = int(mascara_rede[1])
            mascara_rede3 = int(mascara_rede[2])
            mascara_rede4 = int(mascara_rede[3])
        except ValueError:
            print("Erro na máscara! novamente...")
            time.sleep(3)
            os.system('cls')
            continue

        if not (0 <= mascara_rede1 <= 255 and 0 <= mascara_rede2 <= 255 and 0 <= mascara_rede3 <= 255 and 0 <= mascara_rede4 <= 255):
            print("Máscara inválida! Digite a máscara corretamente...")
            time.sleep(3)
            os.system('cls')
            continue
        
        rede1 = octeto1 & mascara_rede1
        rede2 = octeto2 & mascara_rede2
        rede3 = octeto3 & mascara_rede3
        rede4 = octeto4 & mascara_rede4

        mascara_rede_invertida1 = 255 - mascara_rede1
        mascara_rede_invertida2 = 255 - mascara_rede2
        mascara_rede_invertida3 = 255 - mascara_rede3
        mascara_rede_invertida4 = 255 - mascara_rede4

        broadcast1 = rede1 | mascara_rede_invertida1
        broadcast2 = rede2 | mascara_rede_invertida2
        broadcast3 = rede3 | mascara_rede_invertida3
        broadcast4 = rede4 | mascara_rede_invertida4

        primeiro_host1 = rede1
        primeiro_host2 = rede2
        primeiro_host3 = rede3
        primeiro_host4 = rede4 + 1

        ultimo_host1 = broadcast1
        ultimo_host2 = broadcast2
        ultimo_host3 = broadcast3
        ultimo_host4 = broadcast4 - 1

        if octeto1 >= 1 and octeto1 <= 127:
            classe = 'A'
            qtd_hosts = 2 ** 24 - 2
            qtd_subredes = 2 ** 8
        elif octeto1 >= 128 and octeto1 <= 191:
            classe = 'B'
            qtd_hosts = 2 ** 16 - 2
            qtd_subredes = 2 ** 8
        elif octeto1 >= 192 and octeto1 <= 223:
            classe = 'C'
            qtd_hosts = 2 ** 8 - 2
            qtd_subredes = 2 ** 8

        if (octeto1 == 10) or (octeto1 == 172 and 16 <= octeto2 <= 31) or (octeto1 == 192 and octeto2 == 168):
            ip_tipo = "privado"
        else:
            ip_tipo = "público"

        print(f"Rede: {rede1}.{rede2}.{rede3}.{rede4}")
        print(f"Broadcast: {broadcast1}.{broadcast2}.{broadcast3}.{broadcast4}")
        print(f"Primeiro Host: {primeiro_host1}.{primeiro_host2}.{primeiro_host3}.{primeiro_host4}")
        print(f"Último Host: {ultimo_host1}.{ultimo_host2}.{ultimo_host3}.{ultimo_host4}")
        print(f"Classe do IP: {classe}")
        
        if classe in ['A', 'B', 'C']:
            print(f"Sub-redes: {qtd_subredes}")
            print(f"Hosts por sub-rede: {qtd_hosts}")
        
        print(f"O endereço IP é: {ip_tipo}")

    continuar = int(input("Quer continuar? Digite 1 pra sim e 0 pra não: "))
    if continuar == 1:
        print("Reiniciando...")
        time.sleep(3)
        os.system('cls')
        continue
    if continuar == 0:
        print("Saindo...")
        time.sleep(3)
        os.system('cls')
        break
    else: 
        print("Escolha errada, reiniciando...")
        time.sleep(3)
        os.system('cls')
        break
