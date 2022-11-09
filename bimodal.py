class bimodal:
    def __init__(self, bits_to_index):
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**bits_to_index
        self.branch_table = [0 for i in range(self.size_of_branch_table)]
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tBimodal")
        print("\tEntradas en el Predictor:\t\t\t\t\t"+str(2**self.bits_to_index))

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

    def predict(self, PC):
        index = int(PC) % self.size_of_branch_table
        branch_table_entry = self.branch_table[index]
        if branch_table_entry in [0,1]:
            return "N"
        else:
            return "T"

    def update(self, PC, result, prediction):
        index = int(PC) % self.size_of_branch_table
        branch_table_entry = self.branch_table[index]

        #Update entry accordingly
        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry

        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry - 1

        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry

        else:
            updated_branch_table_entry = branch_table_entry + 1

        self.branch_table[index] = updated_branch_table_entry

        #Update stats
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1
