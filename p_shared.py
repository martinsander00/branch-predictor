class p_shared:
    def __init__(self, bits_to_index, local_history_register_size):
        self.bits_to_index = bits_to_index

        # Bits de historia local
        self.local_history_register_size = local_history_register_size
        self.size_of_local_history_table = 2**bits_to_index
        self.local_history_table = []

        # Bits del pattern table
        self.patter_table_size = 2**local_history_register_size
        self.pattern_table = [0 for i in range(self.patter_table_size)]

        # Se rellena la tabla de historia local con mini vectores con 0s
        for i in range(0, self.size_of_local_history_table, 1):
            x = [0] * self.local_history_register_size
            self.local_history_table.append(x)        

    # Contadores
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0


    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tlocal de 2 niveles")
        print("\tEntradas en el History Table:\t\t\t\t\t"+str(2**self.bits_to_index))
        print("\tTamaño de los registros de historia local:\t\t\t\t\t"+str(self.local_history_register_size))
        print("\tEntradas en el Pattern Table:\t\t\t\t\t"+str(2**self.local_history_register_size))

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
        index = int(PC) % self.size_of_local_history_table
        local_history_entry = self.local_history_table[index]

        decimal_res = 0
        cont = self.local_history_register_size - 1
        for i in range (0, self.local_history_register_size, 1):
            num = (local_history_entry[i])*(2**cont)
            decimal_res = decimal_res + num
            cont-=1

        pattern_table_entry = self.pattern_table[decimal_res]
        branch_table_entry = pattern_table_entry

        if branch_table_entry in [0,1]:
            return "N"
        else:
            return "T"


    def update(self, PC, result, prediction):
        index = int(PC) % self.size_of_local_history_table
        local_history_entry = self.local_history_table[index]

        decimal_res = 0
        cont = self.local_history_register_size - 1
        for i in range (0, self.local_history_register_size, 1):
            num = (local_history_entry[i])*(2**cont)
            decimal_res = decimal_res + num
            cont-=1

        pattern_table_entry = self.pattern_table[decimal_res]
        branch_table_entry = pattern_table_entry
        #Update entry accordingly

        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry
            local_history_entry.append(0)

        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry - 1
            local_history_entry.append(0)

        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry
            local_history_entry.append(1)

        else:
            updated_branch_table_entry = branch_table_entry + 1
            local_history_entry.append(1)

        local_history_entry.pop(0)
        self.pattern_table[decimal_res] = updated_branch_table_entry

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

