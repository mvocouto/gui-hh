import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit,
                             QPushButton, QGridLayout, QWidget, QComboBox,
                             QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import date
import holidays
from calculos import GerenciadorFeriados, CalculadoraHorasExtras, CalculadoraSalario

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Horas Extras (Qt)")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout(self.central_widget)

        # --- Fontes ---
        fonte_padrao = QFont("Arial", 12)
        fonte_resultado_titulo = QFont("Arial", 12, QFont.Weight.Bold)

        # --- Obter data atual para valores padrão ---
        hoje = date.today()
        mes_atual = hoje.month
        ano_atual = hoje.year

        # --- Campos de Entrada ---
        self.layout.addWidget(QLabel("Mês:", font=fonte_padrao), 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.mes_combo = QComboBox()
        self.mes_combo.addItems([str(i) for i in range(1, 13)])
        self.mes_combo.setCurrentIndex(mes_atual - 1)
        self.layout.addWidget(self.mes_combo, 0, 1)

        self.layout.addWidget(QLabel("Ano:", font=fonte_padrao), 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.ano_combo = QComboBox()
        anos = [str(ano_atual - i) for i in range(5, -1, -1)] + [str(ano_atual + i) for i in range(1, 6)]
        self.ano_combo.addItems(anos)
        self.ano_combo.setCurrentText(str(ano_atual))
        self.layout.addWidget(self.ano_combo, 1, 1)

        self.layout.addWidget(QLabel("Salário Base:", font=fonte_padrao), 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.salario_input = QLineEdit(font=fonte_padrao)
        self.layout.addWidget(self.salario_input, 2, 1)

        self.layout.addWidget(QLabel("Qtd HE (60%):", font=fonte_padrao), 3, 0, Qt.AlignmentFlag.AlignLeft)
        self.he60_input = QLineEdit(font=fonte_padrao)
        self.layout.addWidget(self.he60_input, 3, 1)

        self.layout.addWidget(QLabel("Qtd HE (120%):", font=fonte_padrao), 4, 0, Qt.AlignmentFlag.AlignLeft)
        self.he120_input = QLineEdit(font=fonte_padrao)
        self.layout.addWidget(self.he120_input, 4, 1)

        # --- Botão Calcular ---
        self.calcular_button = QPushButton("Calcular", font=fonte_padrao)
        self.calcular_button.clicked.connect(self.realizar_calculo)
        self.layout.addWidget(self.calcular_button, 5, 0, 1, 2)

        # --- Labels de Resultado ---
        self.layout.addWidget(QLabel("Resultados:", font=fonte_resultado_titulo), 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.resultado_labels = {}
        row_resultado = 7
        resultados_info = [
            "Salário Base:",
            "Horas Extras (60%):",
            "Horas Extras (120%):",
            "Total Horas Extras:",
            "Dias Úteis no Mês:",
            "Domingos no Mês:",
            "Feriados no Mês (RJ):",
            "Total de DSR:",
            "Salário Bruto Total:",
            "INSS:",
            "IRRF:",
            "Salário Líquido Total:",
        ]

        for texto in resultados_info:
            label_texto = QLabel(texto, font=fonte_padrao)
            self.layout.addWidget(label_texto, row_resultado, 0, Qt.AlignmentFlag.AlignLeft)
            label_resultado = QLabel("", font=fonte_padrao)
            self.layout.addWidget(label_resultado, row_resultado, 1, Qt.AlignmentFlag.AlignRight)
            self.resultado_labels[texto] = label_resultado
            row_resultado += 1

        self.feriados_manager = GerenciadorFeriados()
        self.horas_extras_calculator = CalculadoraHorasExtras()
        self.salario_calculator = CalculadoraSalario()

    def realizar_calculo(self):
        try:
            mes = int(self.mes_combo.currentText())
            ano = int(self.ano_combo.currentText())
            salario_base = float(self.salario_input.text())
            horas_extras_60 = float(self.he60_input.text())
            horas_extras_120 = float(self.he120_input.text())
            horas_mensais_contrato = 200  # Assumindo 200 horas contratuais

            dias_uteis_mes, domingos_mes, feriados_mes = self.feriados_manager.get_dias_uteis_domingos_feriados(ano, mes)

            if dias_uteis_mes is None:
                QMessageBox.critical(self, "Erro", "Feriados para o ano selecionado não encontrados.")
                return

            domingos_e_feriados_mes = domingos_mes + feriados_mes

            valor_he_60 = self.horas_extras_calculator.calcular_hora_extra(salario_base, horas_mensais_contrato, 60, horas_extras_60)
            valor_he_120 = self.horas_extras_calculator.calcular_hora_extra(salario_base, horas_mensais_contrato, 120, horas_extras_120)
            valor_total_horas_extras = valor_he_60 + valor_he_120

            valor_dsr = self.horas_extras_calculator.calcular_dsr(valor_total_horas_extras, dias_uteis_mes, domingos_e_feriados_mes)
            salario_bruto_total = salario_base + valor_he_60 + valor_he_120 + valor_dsr
            inss = self.salario_calculator.calcular_inss(salario_bruto_total)
            irrf = self.salario_calculator.calcular_irrf(salario_bruto_total, inss)
            salario_liquido_total = salario_bruto_total - inss - irrf

            self.resultado_labels["Salário Base:"].setText(f"R$ {salario_base:.2f}")
            self.resultado_labels["Horas Extras (60%):"].setText(f"R$ {valor_he_60:.2f} ({horas_extras_60:.1f} horas)")
            self.resultado_labels["Horas Extras (120%):"].setText(f"R$ {valor_he_120:.2f} ({horas_extras_120:.1f} horas)")
            self.resultado_labels["Total Horas Extras:"].setText(f"R$ {valor_total_horas_extras:.2f}")
            self.resultado_labels["Dias Úteis no Mês:"].setText(str(dias_uteis_mes))
            self.resultado_labels["Domingos no Mês:"].setText(str(domingos_mes))
            self.resultado_labels["Feriados no Mês (RJ):"].setText(str(feriados_mes))
            self.resultado_labels["Total de DSR:"].setText(f"R$ {valor_dsr:.2f}")
            self.resultado_labels["Salário Bruto Total:"].setText(f"R$ {salario_bruto_total:.2f}")
            # self.resultado_labels["Salário Bruto Total:"].setText(f"R$ {salario_bruto_total:.2f}")
            self.resultado_labels["INSS:"].setText(f"R$ {inss:.2f}")
            self.resultado_labels["IRRF:"].setText(f"R$ {irrf:.2f}")
            self.resultado_labels["Salário Líquido Total:"].setText(f"R$ {salario_liquido_total:.2f}")

        except ValueError:
            QMessageBox.critical(self, "Erro", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())