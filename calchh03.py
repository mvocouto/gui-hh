import holidays
from datetime import date

def calcular_inss(salario_bruto):
    """Calcula o valor da contribuição ao INSS com base nas alíquotas de 2025."""
    if salario_bruto <= 1412.00:
        return salario_bruto * 0.075
    elif salario_bruto <= 2666.64:
        return salario_bruto * 0.09 - 21.18
    elif salario_bruto <= 4000.39:
        return salario_bruto * 0.12 - 80.38
    elif salario_bruto <= 7786.02:
        return salario_bruto * 0.14 - 160.78
    else:
        return 7786.02 * 0.14 - 160.78  # Teto do INSS

def calcular_irrf(salario_base, inss):
    """Calcula o valor do Imposto de Renda Retido na Fonte (IRRF) com base nas alíquotas de 2025."""
    base_calculo = salario_base - inss
    if base_calculo <= 2259.20:
        return 0.0
    elif base_calculo <= 2826.65:
        return base_calculo * 0.075 - 169.44
    elif base_calculo <= 3751.05:
        return base_calculo * 0.15 - 381.44
    elif base_calculo <= 4664.68:
        return base_calculo * 0.225 - 662.77
    else:
        return base_calculo * 0.275 - 896.00

def calcular_hora_extra(salario_base, horas_trabalhadas_mes, adicional_percentual, horas_extras):
    """Calcula o valor das horas extras com um determinado adicional."""
    if horas_trabalhadas_mes <= 0:
        return "Erro: O número de horas trabalhadas no mês deve ser maior que zero."
    if horas_extras < 0:
        return "Erro: O número de horas extras não pode ser negativo."

    valor_hora_normal = salario_base / horas_trabalhadas_mes
    valor_hora_extra = valor_hora_normal * (1 + (adicional_percentual / 100))
    valor_total_horas_extras = valor_hora_extra * horas_extras
    return valor_total_horas_extras

def calcular_dsr_sobre_he(valor_total_horas_extras, dias_uteis):
    """Calcula o valor do Descanso Semanal Remunerado (DSR) sobre as horas extras."""
    if dias_uteis <= 0:
        return 0.0
    # O número de domingos e feriados será calculado fora da função
    return (valor_total_horas_extras / dias_uteis)

def get_dias_uteis_domingos_feriados(ano, mes):
    """Calcula os dias úteis, domingos e feriados no Brasil (RJ) para um dado mês e ano."""
    rj_holidays = holidays.CountryHoliday("BR", state="RJ", years=ano)
    dias_uteis = 0
    domingos = 0
    feriados = 0
    num_dias_mes = (date(ano, mes + 1, 1) - date(ano, mes, 1)).days if mes < 12 else (date(ano + 1, 1, 1) - date(ano, mes, 1)).days

    for dia in range(1, num_dias_mes + 1):
        data = date(ano, mes, dia)
        dia_semana = data.weekday()  # Segunda é 0 e Domingo é 6
        if data in rj_holidays:
            feriados += 1
        elif dia_semana == 6:
            domingos += 1
        else:
            dias_uteis += 1

    return dias_uteis, domingos, feriados

# *** INSERA SEUS DADOS AQUI ***
seu_salario_base = 13500.00
suas_horas_mensais_contrato = 200
suas_horas_extras_60 = 0.0
suas_horas_extras_120 = 15.0
ano_calculo = 2025
mes_calculo = 5  # Maio (1 para Janeiro, 12 para Dezembro)

# *** OBTENDO DIAS ÚTEIS, DOMINGOS E FERIADOS ***
dias_uteis_mes, domingos_mes, feriados_mes = get_dias_uteis_domingos_feriados(ano_calculo, mes_calculo)
domingos_e_feriados_mes = domingos_mes + feriados_mes

# *** CÁLCULOS DAS HORAS EXTRAS ***
valor_he_60 = calcular_hora_extra(seu_salario_base, suas_horas_mensais_contrato, 60, suas_horas_extras_60)
valor_he_120 = calcular_hora_extra(seu_salario_base, suas_horas_mensais_contrato, 120, suas_horas_extras_120)
valor_total_horas_extras = valor_he_60 + valor_he_120

# *** CÁLCULO DO DSR SOBRE AS HORAS EXTRAS ***
valor_dsr = calcular_dsr_sobre_he(valor_total_horas_extras, dias_uteis_mes) * domingos_e_feriados_mes

# Salário bruto total
salario_bruto_total = seu_salario_base + valor_he_60 + valor_he_120 + valor_dsr

# Cálculo dos descontos
inss = calcular_inss(salario_bruto_total)
irrf = calcular_irrf(seu_salario_base, inss)

# Salário líquido total
salario_liquido_total = salario_bruto_total - inss - irrf

# *** EXIBIÇÃO DOS RESULTADOS ***
print(f"Cálculo para o mês {mes_calculo}/{ano_calculo}")
print(f"Salário Base: R$ {seu_salario_base:.2f}")
print(f"Horas Extras (60%): R$ {valor_he_60:.2f} ({suas_horas_extras_60} horas)")
print(f"Horas Extras (120%): R$ {valor_he_120:.2f} ({suas_horas_extras_120} horas)")
print(f"Total Horas Extras: R$ {valor_total_horas_extras:.2f}")
print(f"Dias Úteis no Mês: {dias_uteis_mes}")
print(f"Domingos no Mês: {domingos_mes}")
print(f"Feriados no Mês (RJ): {feriados_mes}")
print(f"Total de Domingos e Feriados: {domingos_e_feriados_mes}")
print(f"DSR sobre Horas Extras: R$ {valor_dsr:.2f}")
print(f"Salário Bruto Total: R$ {salario_bruto_total:.2f}")
print(f"INSS: R$ {inss:.2f}")
print(f"IRRF: R$ {irrf:.2f}")
print(f"Salário Líquido Total: R$ {salario_liquido_total:.2f}")