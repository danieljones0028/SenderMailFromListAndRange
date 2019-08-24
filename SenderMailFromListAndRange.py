# -*- coding: utf-8 -*-

import smtplib
import os
import sys
import subprocess
import datetime
from time import sleep
import logging

logging.basicConfig(filename='senderforms.log', format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

#######################################CONFIG##################################
#######################################PATH####################################
path_list = 'Lista.txt'
path_senders = 'enviados.txt'
path_newlist = 'nova_lista.txt'
#######################################SMTP####################################
smtp_server = 'smtp.dominio.com.br'
port = 587
sender = 'sender@dominio.com.br'
passwd = 'PASSWD'
Subject = "Subject"
aviso_termino = "aviso@dominio.com.br"
text = """

texto texto texto

"""
#######################################CONFIG##################################

def list_twohundred():

    try:
        if os.path.exists(path_list):
            lista = open(path_list, 'r').read().split('\n')
            del lista[-1]

            if len(lista) <= 200:
                sends = len(lista)
            else:
                sends = 200
            return sends
        else:
            print(f'Ocorreu um erro ao tentar ler o arquivo lista.txt.\nPor favor verifique se o mesmo existe e se tem permissão de leitura do mesmo.\n')
            logging.info(f'TRATAMENTO DA LISTA - Ocorreu um erro ao tentar ler o arquivo lista.txt. Por favor verifique se o mesmo existe e se tem permissão de leitura do mesmo.')
            sys.exit(1)
    except FileNotFoundError:
        print(f'Ocorreu um erro ao tentar ler o arquivo lista.txt na primeira definição\nPor favor verifique se o mesmo existe e se tem permissão de leitura do mesmo.\n')

def sendfor_hour(end):

    try:
        if os.path.exists(path_list):
            lista = open(path_list, 'r').read().split('\n')
            del lista[-1]
    except FileNotFoundError:
        print(f'Ocorreu um erro ao tentar ler o arquivo lista.txt na segunda definição\nPor favor verifique se o mesmo existe e se tem permissão de leitura do mesmo.\n')
        logging.info(f'ENVIO - Ocorreu um erro ao tentar ler o arquivo lista.txt. Por favor verifique se o mesmo existe e se tem permissão de leitura do mesmo.')
        sys.exit(1)

    for send in range(0, end):
        if send != '':
            if send == end:
                print('Numero maximo de envios alcançado.')
                logging.info(f'Numero maximo de envios alcançado: {end}')
                break
            else:
                try:
                    server = smtplib.SMTP(f'{smtp_server}', f'{port}')
                    server.ehlo()
                    server.starttls()
                    logging.info('Verificando o servidor de envio...')
                    logging.info('O.K')
                except:
                    print('Servidor de envio indisponivel.')
                    logging.warning('Servidor de envio indisponivel.')
                    sys.exit(0)

                try:
                    server.login(f"{sender}", f"{passwd}")

                    data = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z')

                    From = f"{sender}"
                    subject = f"{Subject}"
                    texto = f"{text}"

                    msg = "\r\n".join([
                        f"From: {From}",
                        f"To: {lista[send]}",
                        f"Subject: {subject}",
                        f"Date: {data}"
                        "",
                        f"{texto}"
                    ])

                    logging.info(f'Enviando e-mail para: {lista[send]}')
                    server.sendmail(f"{From}", {lista[send]}, msg.encode('utf-8'))
                    server.quit()
                    logging.info(f'E-mail enviado com sucesso para: {lista[send]}')
                    print(lista[send])
                    senders = (path_senders)
                    s = open(senders, 'a')
                    s.write(f'{lista[send]}\n')
                    s.close()
                    logging.warning('Arquivo de registro de enviados criado com sucesso')
                except IndexError:
                    print('Lista esta vazia')
                    logging.warning('A lista não contem dados')
                    sys.exit(1)

def update_list():
    try:
        if os.path.exists(path_senders):
            lista_atual = open(path_list, 'r').read().split('\n')
            lista_enviados = open(path_senders, 'r').read().split('\n')

        for new_list in lista_atual:
            if new_list not in lista_enviados:
                new = (path_newlist)
                n = open(new, 'a')
                n.write(f'{new_list}\n')
                n.close()

        if os.path.exists(path_list):
            lista_atual = (path_list)

        if os.path.exists(path_newlist):
            new = (path_newlist)
            new_file = f'cat {new} > {lista_atual}'
            subprocess.check_call([new_file], shell=True)
        else:
            print('nao tem nada na diferenca')
            try:
                server = smtplib.SMTP('smtp.dominio.com.br', 587)
                server.ehlo()
                server.starttls()
            except:
                print('Algo deu errado no login.')

            try:
                server.login(f"{sender}", f"{passwd}")

                data = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z')

                From = f"{sender}"
                from_return = f"{aviso_termino}"
                subject = "Finalizado o serviço de envio de e-mails automaticos."
                texto = """

O Ultimo e-mail foi enviado

"""

                msg = "\r\n".join([
                    f"From: {From}",
                    f"To: {from_return}",
                    f"Subject: {subject}",
                    f"Date: {data}"
                    "",
                    f"{texto}"
                ])

                logging.warning(f'Enviando notificação de terminio de lista de envio para: {from_return}')
                server.sendmail(f"{From}", f"{from_return}", msg.encode('utf-8'))
                server.quit()
                logging.info(f'Notificação enviada com sucesso: {from_return}')

                clean_lista()
                logging.info(f'Limpando lista atual')
                clean_home()
                logging.info(f'Limpando arquivos criados na execução do script.')
                sys.exit(0)
            except TypeError as e:
                print(e)
                logging.warning(f'ERRO - {e}')
    except:
        pass

def clean_home():
    try:
        nl = (path_newlist)
        ev = (path_senders)
        if os.path.exists(nl):
            cleanup_one = f'rm -f {nl}'
            subprocess.check_call([cleanup_one], shell=True)
            logging.info(f'Deletando o arquivo {nl}')
        if os.path.exists(ev):
            cleanup_two = f'rm -f {ev}'
            subprocess.check_call([cleanup_two], shell=True)
            logging.info(f'Deletando o arquivo {ev}')
    except:
        print(f'Arquivos {nl} e {ev} não encontrados')
        logging.warning(f'Arquivos {nl} e {ev} não encontrados')
    finally:
        nl = (path_newlist)
        ev = (path_senders)
        if os.path.exists(nl):
            cleanup_one = f'rm -f {nl}'
            subprocess.check_call([cleanup_one], shell=True)
            logging.info(f'Forçando o delete do arquivo {nl}')
        if os.path.exists(ev):
            cleanup_two = f'rm -f {ev}'
            subprocess.check_call([cleanup_two], shell=True)
            logging.info(f'Forçando o delete do arquivo {ev}')

def clean_lista():
    try:
        lt = (path_list)
        if os.path.exists(lt):
            cleanup_one = f'rm -f {lt}'
            subprocess.check_call([cleanup_one], shell=True)
            logging.info(f'Deletando o arquivo {lt}')
    except:
        print(f'Arquivos {lt} não encontrados')
        logging.info(f'Arquivos {lt} não encontrados')

def check_filivelist():
    try:
        contador = 0
        while os.path.exists(path_list):
            print('A lista ainda existe, esperando uma hora e dez minutos.')
            logging.info('A lista ainda existe, esperando uma hora e dez minutos.')
            sleep(4200)
            logging.info('Tempo de espera acabou iniciando o envio.')
            list_twohundred()
            sendfor_hour(list_twohundred())
            update_list()
            clean_home()
            contador = contador + 1
            print(f'loop ja foi realizado {contador} vezes.')
            print(f'Enviados {contador * 200} e-mails.')
            logging.info(f'loop ja foi realizado {contador} vezes.')
            logging.info(f'Enviados {contador * 200} e-mails.')
        else:
            print('Tudo Ok finalizando')
            sys.exit(0)
    except TypeError as e:
        print(e)


list_twohundred()
sendfor_hour(list_twohundred())
update_list()
clean_home()
check_filivelist()
