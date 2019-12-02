"""Validador de registro de execução"""
import sys

def main():
    leitores = 0
    escritores = 0
    leitores_correntes = []
    escritor_corrente = -1
    leitores_tent = []
    escritores_tent = []
    recurso = -1
    turno_do_leitor = 1

    def leitor_tentando(tid):
        nonlocal leitores_tent
        leitores_tent.append(tid)

    def leitor_bloq(tid, fila_escr, turno):
        if not escritores and (fila_escr > 0 and turno == 0):
            print('[✓] Leitor', tid, 'bloqueado por haver fila de escritores e não ter prioridade')

    def leitor_voltando(tid):
        if tid not in leitores_tent:
            print('[✕] Leitor', tid, 'voltou de bloqueio sem ter sido bloqueado')
            sys.exit(1)

    def leitor_entrou(tid, num_de_leitores, turno):
        nonlocal leitores, leitores_correntes, leitores_tent, escritores
        leitores = leitores + 1

        if leitores != num_de_leitores:
            print('[✕] Número incompatível de leitores.')
            sys.exit(1)

        if escritores > 0:
            print('[✕] Leitor entrou enquanto escritor escrevia')
            sys.exit(1)

        if len(escritores_tent) > 0 and turno == 0:
            print('[✕] Leitor entrou fora de turno enquanto havia escritores esperando.')
            sys.exit(1)

        leitores_tent.remove(tid)
        leitores_correntes.append(tid)

    def leitor_saiu(tid, rec):
        nonlocal leitores, leitores_correntes, turno_do_leitor
        leitores = leitores - 1

        if recurso != rec:
            print('[✕] Leitor não leu um valor correto.')
            sys.exit(1)

        turno_do_leitor = 0

        leitores_correntes.remove(tid)

    def escritor_tentando(tid):
        nonlocal escritores_tent
        escritores_tent.append(tid)

    def escritor_bloq(tid, fila_leit, turno):
        if not escritores and (fila_leit > 0 and turno == 1):
            print('[✓] Escritor', tid, 'bloqueado por haver fila de leitores e não ter prioridade')

    def escritor_voltando(tid):
        if not tid in escritores_tent:
            print('[✕] Escritor', tid, 'voltou de bloqueio sem ter sido bloqueado')
            sys.exit(1)

    def escritor_entrou(tid, turno):
        nonlocal escritor_corrente, escritores_tent, escritores, turno_do_leitor

        if escritor_corrente != -1 or len(leitores_correntes) > 0:
            print('[✕] Escritor entrou com leitores ou escritor já ativo.')
            sys.exit(1)

        if len(leitores_tent) > 0 and turno == 1:
            print('[✕] Escritor entrou fora de vez com leitores esperando.')
            sys.exit(1)

        escritores = escritores + 1
        escritores_tent.remove(tid)
        escritor_corrente = tid

    def escritor_saiu(tid, rec):
        nonlocal escritor_corrente, escritores, recurso, turno_do_leitor
        if escritor_corrente != tid:
            print('[✕] Escritor que saiu não é o escritor ativo.')
            sys.exit(1)

        turno_do_leitor = 1
        recurso = rec
        escritor_corrente = -1
        escritores = escritores - 1


    if len(sys.argv) < 2:
        print('[✕] Digite "python', sys.argv[0], '<nome do arquivo de log>"')
        sys.exit(1)

    with open(sys.argv[1]) as log:
        for linha in log:
            exec(linha)

    print('[✓] Ok!')

if __name__ == '__main__':
    main()
