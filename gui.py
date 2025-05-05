import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import holidays
from calculos import GerenciadorFeriados, CalculadoraHorasExtras, CalculadoraSalario

class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Horas Extras")

        # --- Configuração da Fonte ---
        fonte_padrao = ('Arial', 12)
        fonte_resultado_titulo = ('Arial', 12, 'bold')
        style = ttk.Style(root)
        style.configure('TLabel', font=fonte_padrao)
        style.configure('TEntry', font=fonte_padrao)
        style.configure('TButton', font=fonte_padrao)
        style.configure('TCombobox', font=fonte_padrao)
        style.configure('Resultado.TLabel', font=fonte_resultado_titulo)

        # --- Definir Tamanho Mínimo da Janela ---
        root.minsize(400, 540)  # Aumentando a altura mínima para acomodar mais labels

        # --- Obter data atual para valores padrão ---
        hoje = date.today()
        mes_atual = hoje.month
        ano_atual = hoje.year

        # --- Campos de Entrada ---
        ttk.Label(root, text="Mês:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.mes_options = list(range(1, 13))
        self.mes_entry = ttk.Combobox(root, values=self.mes_options, width=5)
        self.mes_entry.set(mes_atual)
        self.mes_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(root, text="Ano:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.ano_options = list(range(ano_atual - 5, ano_atual + 6))  # Opções de ano para +/- 5 anos
        self.ano_entry = ttk.Combobox(root, values=self.ano_options, width=7)
        self.ano_entry.set(ano_atual)
        self.ano_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(root, text="Salário Base:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.salario_entry = ttk.Entry(root)
        self.salario_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(root, text="Qtd HE (60%):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.he60_entry = ttk.Entry(root)
        self.he60_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(root, text="Qtd HE (120%):").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.he120_entry = ttk.Entry(root)
        self.he120_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)

        # --- Botão Calcular ---
        calcular_button = ttk.Button(root, text="Calcular", command=self.calcular_tudo)
        calcular_button.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Separator(root).grid(row=6, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)

        # --- Labels de Resultado ---
        self.resultado_labels = {}
        row_resultado = 7
        resultados_info = {
            "Salário Base:": tk.StringVar(),
            "Horas Extras (60%):": tk.StringVar(),
            "Horas Extras (120%):": tk.StringVar(),
            "Total Horas Extras:": tk.StringVar(),
            "Dias Úteis no Mês:": tk.StringVar(),
            "Domingos no Mês:": tk.StringVar(),
            "Feriados no Mês (RJ):": tk.StringVar(),
            "Total de DSR:": tk.StringVar(),
            "Salário Bruto Total:": tk.StringVar(),
            "INSS:": tk.StringVar(),
            "IRRF:": tk.StringVar(),
            "Salário Líquido Total:": tk.StringVar(),
        }

        for texto, var in resultados_info.items():
            ttk.Label(root, text=texto).grid(row=row_resultado, column=0, sticky=tk.W, padx=5, pady=2)
            lbl_resultado = ttk.Label(root, textvariable=var, anchor='e')
            lbl_resultado.grid(row=row_resultado, column=1, sticky=tk.EW, padx=5, pady=2)
            self.resultado_labels[texto] = var
            row_resultado += 1

    def calcular_tudo(self):
        try:
            mes = int(self.mes_entry.get())
            ano = int(self.ano_entry.get())
            salario_base = float(self.salario_entry.get())
            horas_extras_60 = float(self.he60_entry.get())
            horas_extras_120 = float(self.he120_entry.get())
            horas_mensais_contrato = 200  # Assumindo 200 horas contratuais

            feriados_manager = GerenciadorFeriados()
            dias_uteis_mes, domingos_mes, feriados_mes = feriados_manager.get_dias_uteis_domingos_feriados(ano, mes)

            if dias_uteis_mes is None:
                for var in self.resultado_labels.values():
                    var.set("Erro ao obter informações de feriados.")
                return

            domingos_e_feriados_mes = domingos_mes + feriados_mes

            horas_extras_calculator = CalculadoraHorasExtras()
            valor_he_60 = horas_extras_calculator.calcular_hora_extra(salario_base, horas_mensais_contrato, 60, horas_extras_60)
            valor_he_120 = horas_extras_calculator.calcular_hora_extra(salario_base, horas_mensais_contrato, 120, horas_extras_120)
            valor_total_horas_extras = valor_he_60 + valor_he_120

            salario_calculator = CalculadoraSalario()
            valor_dsr = horas_extras_calculator.calcular_dsr(valor_total_horas_extras, dias_uteis_mes, domingos_e_feriados_mes)
            salario_bruto_total = salario_base + valor_he_60 + valor_he_120 + valor_dsr
            inss = salario_calculator.calcular_inss(salario_bruto_total)
            irrf = salario_calculator.calcular_irrf(salario_bruto_total, inss)
            salario_liquido_total = salario_bruto_total - inss - irrf

            self.resultado_labels["Salário Base:"].set(f"R$ {salario_base:.2f}")
            self.resultado_labels["Horas Extras (60%):"].set(f"R$ {valor_he_60:.2f} ({horas_extras_60} horas)")
            self.resultado_labels["Horas Extras (120%):"].set(f"R$ {valor_he_120:.2f} ({horas_extras_120} horas)")
            self.resultado_labels["Total Horas Extras:"].set(f"R$ {valor_total_horas_extras:.2f}")
            self.resultado_labels["Dias Úteis no Mês:"].set(dias_uteis_mes)
            self.resultado_labels["Domingos no Mês:"].set(domingos_mes)
            self.resultado_labels["Feriados no Mês (RJ):"].set(feriados_mes)
            self.resultado_labels["Total de DSR:"].set(f"R$ {valor_dsr:.2f}")
            self.resultado_labels["Salário Bruto Total:"].set(f"R$ {salario_bruto_total:.2f}")
            self.resultado_labels["INSS:"].set(f"R$ {inss:.2f}")
            self.resultado_labels["IRRF:"].set(f"R$ {irrf:.2f}")
            self.resultado_labels["Salário Líquido Total:"].set(f"R$ {salario_liquido_total:.2f}")

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()