from module_teo_nicolas.lib.qsoccer import QSoccer

nb_player_per_team = 2
qsoccer = QSoccer.get_instance(nb_player_per_team)

qsoccer.Train(show=False)
qsoccer.printBestsAndWorsts()