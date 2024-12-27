
# from main import MyWidget


class CPLFrequencyManager:
    def __init__(self, freq_central, pilote_hf=0, service_bf=0, freq_gl=0):
        self.freq_central = freq_central
        self.pilote_hf = pilote_hf
        self.service_bf = service_bf
        self.freq_gl = freq_gl
        self.results = self._calculate_frequencies()

    def _validate_inputs(self):
        if not isinstance(self.freq_central, int):
            raise TypeError("freq_central must be an integer.")
        if not (40 <= self.freq_central <= 500):
            raise ValueError("freq_central must be between 40 and 500.")

        for param_name, param_value in [("pilote_hf", self.pilote_hf), ("service_bf", self.service_bf), ("freq_gl", self.freq_gl)]:
            if not isinstance(param_value, (int, float)):
                raise TypeError(f"{param_name} must be a float or an integer.")
            if not (0 <= param_value <= 4):
                raise ValueError(f"{param_name} must be between 0 and 4.")

    def _calculate_frequencies(self):
        self._validate_inputs()
        freq_voice = [-8, -4, 0, 4, 8]
        list_of_freqs = [self.freq_central + fv for fv in freq_voice]

        reception_ph_results = {
            "Rx2": {
                "voie_direct": list_of_freqs[0] + self.pilote_hf,
                "voie_inversée": list_of_freqs[1] - self.pilote_hf,
            },
            "Rx1": {
                "voie_direct": list_of_freqs[1] + self.pilote_hf,
                "voie_inversée": list_of_freqs[2] - self.pilote_hf,
            },
        }

        emission_ph_results = {
            "Tx1": {
                "voie_direct": list_of_freqs[2] + self.pilote_hf,
                "voie_inversée": list_of_freqs[3] - self.pilote_hf,
            },
            "Tx2": {
                "voie_direct": list_of_freqs[3] + self.pilote_hf,
                "voie_inversée": list_of_freqs[4] - self.pilote_hf,
            },
        }

        reception_bf_results = {
            "Rx2": {
                "voie_direct": list_of_freqs[0] + self.service_bf,
                "voie_inversée": list_of_freqs[1] - self.service_bf,
            },
            "Rx1": {
                "voie_direct": list_of_freqs[1] + self.service_bf,
                "voie_inversée": list_of_freqs[2] - self.service_bf - self.freq_gl,
            },
        }

        emission_bf_results = {
            "Tx1": {
                "voie_direct": list_of_freqs[2] + self.service_bf + self.freq_gl,
                "voie_inversée": list_of_freqs[3] - self.service_bf,
            },
            "Tx2": {
                "voie_direct": list_of_freqs[3] + self.service_bf,
                "voie_inversée": list_of_freqs[4] - self.service_bf,
            },
        }

        results = {
            "reception_ph_results": reception_ph_results,
            "emission_ph_results": emission_ph_results,
            "reception_bf_results": reception_bf_results,
            "emission_bf_results": emission_bf_results,
        }
        # print("DEBUG: Calculated Results:", results)  # Debug statement
        return results

    # def voie_choice(self, selected_options):
        # self.model = selected_options.get("Type du CPL", "")
        # self.tx1 = selected_options.get("Type de voie (Emission Voie I)", "")
        # self.tx2 = selected_options.get("Type de voie (Emission Voie II)", "")
        # self.rx1 = selected_options.get("Type de voie (Reception Voie I)", "")
        # self.rx2 = selected_options.get("Type de voie (Reception Voie II)", "")
        # print(self.model, self.tx1, self.tx2, self.rx1, self.rx2)

    def display_results(self, selected_options):
        self.model = selected_options.get("Type du CPL", "")
        self.tx1 = selected_options.get("Type de voie (Emission Voie I)", "")
        self.tx2 = selected_options.get("Type de voie (Emission Voie II)", "")
        self.rx1 = selected_options.get("Type de voie (Reception Voie I)", "")
        self.rx2 = selected_options.get("Type de voie (Reception Voie II)", "")
        # print(self.model, self.tx1, self.tx2, self.rx1, self.rx2)

        cpl_equipement = ["S2/S3", "OPC-1",
                          "OPC-2", "STE-N", "ALSPA 1790B", "T390"]
        # Initialize default values to avoid KeyError
        tx1_ph, tx2_ph, rx1_ph, rx2_ph = None, None, None, None
        tx1_bf, tx2_bf, rx1_bf, rx2_bf = None, None, None, None

        if self.model in cpl_equipement[0]:  # S2/S3
            # Pilote HF Emission/Reception
            tx1_ph = self.results["emission_ph_results"]["Tx1"][self.tx1]
            rx1_ph = self.results["reception_ph_results"]["Rx1"][self.rx1]
            # Service BF Emission/Reception
            tx1_bf = self.results["emission_bf_results"]["Tx1"][self.tx1]
            rx1_bf = self.results["reception_bf_results"]["Rx1"][self.rx1]

        elif self.model in cpl_equipement[1]:  # OPC-1
            # Pilote HF Emission/Reception
            tx1_ph = self.results["emission_ph_results"]["Tx1"][self.tx1]
            rx1_ph = self.results["reception_ph_results"]["Rx1"][self.rx1]
            # Service BF Emission/Reception
            tx1_bf = self.results["emission_bf_results"]["Tx1"][self.tx1]
            rx1_bf = self.results["reception_bf_results"]["Rx1"][self.rx1]

        elif self.model in cpl_equipement[2]:  # OPC-2
            # Pilote HF Emission
            tx1_ph = self.results["emission_ph_results"]["Tx1"][self.tx1]
            tx2_ph = self.results["emission_ph_results"]["Tx2"][self.tx2]
            # Pilote HF Reception
            rx1_ph = self.results["reception_ph_results"]["Rx1"][self.rx1]
            rx2_ph = self.results["reception_ph_results"]["Rx2"][self.rx2]
            # Service BF Emission
            tx1_bf = self.results["emission_bf_results"]["Tx1"][self.tx1]
            tx2_bf = self.results["emission_bf_results"]["Tx2"][self.tx2]
            # Service BF Reception
            rx1_bf = self.results["reception_bf_results"]["Rx1"][self.rx1]
            rx2_bf = self.results["reception_bf_results"]["Rx2"][self.rx2]

        # STE-N or ALSPA 1790B
        elif self.model in cpl_equipement[3] or self.model == cpl_equipement[4]:
            # Pilote HF Emission
            tx1_ph = self.results["emission_ph_results"]["Tx1"]["voie_inversée"]
            # Pilote HF Reception
            rx1_ph = self.results["reception_ph_results"]["Rx1"]["voie_direct"]
            # Service BF Emission
            tx1_bf = self.results["emission_bf_results"]["Tx1"]["voie_inversée"]
            tx2_bf = self.results["emission_bf_results"]["Tx2"]["voie_direct"]
            # Service BF Reception
            rx1_bf = self.results["reception_bf_results"]["Rx2"]["voie_inversée"]
            rx2_bf = self.results["reception_bf_results"]["Rx1"]["voie_direct"]

        elif self.model in cpl_equipement[5]:  # T390
            # Pilote HF Emission
            tx1_ph = self.results["emission_ph_results"]["Tx2"]["voie_inversée"]
            # Pilote HF Reception
            rx1_ph = self.results["reception_ph_results"]["Rx2"]["voie_direct"]
            # Service BF Emission
            tx1_bf = self.results["emission_bf_results"]["Tx1"]["voie_direct"]
            # Service BF Reception
            rx1_bf = self.results["reception_bf_results"]["Rx1"]["voie_inversée"]

        results_to_display = {
            "tx1_ph": tx1_ph,
            "tx2_ph": tx2_ph,
            "rx1_ph": rx1_ph,
            "rx2_ph": rx2_ph,
            "tx1_bf": tx1_bf,
            "tx2_bf": tx2_bf,
            "rx1_bf": rx1_bf,
            "rx2_bf": rx2_bf
        }
        # print("DEBUG: Calculated Results:", results)  # Debug statement
        return results_to_display
