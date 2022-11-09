from g_shared import *
from p_shared import *

class torneo:
    def __init__(self, bits_to_index, global_history_size, local_history_register_size):
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**bits_to_index
        self.branch_table = [0 for i in range(self.size_of_branch_table)]
        self.p_shared = p_shared(bits_to_index, local_history_register_size)
        self.g_shared = g_shared(bits_to_index, global_history_size)

        # Predicciones
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0
        self.counter = 0

    def predict(self, PC):
        prediction_p = self.p_shared.predict(PC)
        prediction_g = self.g_shared.predict(PC)

        return prediction_p, prediction_g

    def update(self, PC, result, prediction_p, prediction_g):

        self.p_shared.update(PC, result, prediction_p)
        self.g_shared.update(PC, result, prediction_g)

        if self.counter in [1,0]:
            prediction = prediction_p

        else:
            prediction = prediction_g

        #Update entry accordingly
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1

        if (result == prediction_g) and (prediction_g != prediction_p):
            if self.counter < 3:
                self.counter += 1

        elif (result == prediction_p) and (prediction_g != prediction_p):
            if self.counter > 0:
                self.counter += -1

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tGlobal de 2 niveles")
        print("\tEntradas en el Predictor Global:\t\t\t\t\t"+str(2**self.bits_to_index))
        # print("\tTamaño de los registros de historia global:\t\t\t\t\t"+str(self.g_shared))
        print("\tEntradas en el History Table:\t\t\t\t\t"+str(2**self.bits_to_index))
        # print("\tTamaño de los registros de historia local:\t\t\t\t\t"+str(self.p_shared))
        # print("\tEntradas en el Pattern Table:\t\t\t\t\t"+str(2**self.p_shared))

    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")