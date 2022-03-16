# import threading
#
# from tesseract_war_thunder.scan.crowler import crowl_player_stats
#
#
# class SimpleThread(threading.Thread):
#
#     def __init__(self, player):
#         threading.Thread.__init__(self)
#         self.player = player
#         self.stats = None
#
#     def run(self):
#         print("Starting " + self.name)
#         z = crowl_player_stats(self.player.player_nick)
#         print("Exiting " + self.name)
#         return z
