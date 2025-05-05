from datetime import date
import holidays

class GerenciadorFeriados:
    def get_dias_uteis_domingos_feriados(self, ano, mes):
        """Calcula os dias úteis, domingos e feriados no Brasil (RJ) para um dado mês e ano."""
        try:
            rj_holidays = holidays.CountryHoliday('BR', state='RJ', years=ano)
        except KeyError:
            messagebox.showerror("Erro", f"Feriados para o ano {ano} não encontrados na biblioteca.")
            return None, None, None

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

class CalculadoraHorasExtras:
    def calcular_hora_extra(self, salario_base, horas_trabalhadas_mes, adicional_percentual, horas_extras):
        """Calcula o valor das horas extras com um determinado adicional."""
        if horas_trabalhadas_mes <= 0 or horas_extras < 0:
            return 0.0  # Ou lançar uma exceção

        valor_hora_normal = salario_base / horas_trabalhadas_mes
        valor_hora_extra = valor_hora_normal * (1 + (adicional_percentual / 100))
        return valor_hora_extra * horas_extras

    def calcular_dsr(self, valor_total_horas_extras, dias_uteis, domingos_feriados):
        """Calcula o valor do Descanso Semanal Remunerado (DSR)."""
        if dias_uteis <= 0:
            return 0.0
        return (valor_total_horas_extras / dias_uteis) * domingos_feriados

class CalculadoraSalario:
    def calcular_inss(self, salario_bruto):
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

    def calcular_irrf(self, salario_base, inss):
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