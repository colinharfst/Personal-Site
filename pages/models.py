from django.db import models
import datetime
import mlbgame
import xml.etree.cElementTree as etree
import requests

class DarkMode(models.Model):
	val = models.IntegerField(default=0)
	
	def inc(self):
		if self.val == 0:
			self.val = 1
			return self.val
		else:
			self.val = 0
			return self.val


class Judge(models.Model):
	
	lastGameVal = models.IntegerField(default=-1)
	lastHRDate = models.DateTimeField('lastHRDate')

	def didJudgeHR(self):

		today = datetime.datetime.today() #datetime.datetime(2019, 4, 8, 20, 00)
		game_array = mlbgame.games(today.year, today.month, today.day, home='Yankees', away='Yankees')
		print(game_array)

		if game_array != []:
			print('duh')
			print(len(game_array))
			print(len(game_array[0]))
			if len(game_array[0]) == 1:
				print('huh')
				game = game_array[0][0]
				game_id = game.game_id
				if (today.month < 10):
					if (today.day < 10):
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_0" + str(today.month) + "/day_0" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"
					else:
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_0" + str(today.month) + "/day_" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"
				else:
					if (today.day < 10):
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_" + str(today.month) + "/day_0" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"
					else:
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_" + str(today.month) + "/day_" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"

				tree = etree.fromstring(requests.get(url).text)

				if (game.home_team == 'Yankees'):
					batting_stats = tree.findall('batting')[0]
				else:
					batting_stats = tree.findall('batting')[1]

				for batter in batting_stats:
					if (batter.get('id') == '592450'):
						print ('here')
						if (int(batter.get('hr')) == 0):
							print ('here')
							if game.game_status == 'FINAL':
								# If the game is over, treat it as such
								self.lastGameVal = 0
								return 0
							else:
								# If the game is not over, treat it as if there has been no game yet today
								return 999
						else:
							# If he's homered, we don't care if the game is over
							self.lastGameVal = batter.get('hr')
							self.lastHRDate = today
							return int(batter.get('hr'))
				if game.game_status == 'FINAL':
					print('here')
					# If Judge isn't in batting_stats, but the game is over, treat it as such
					self.lastGameVal = 0
					return 0
				else:
					# If Judge isn't in batting_stats, but the game is not over, treat it as if there has been no game yet today
					return 999

			# DOUBLE HEADER MEANS DOUBLE CODDDDDDDDDEEEEEEEEE
			if (len(game_array[0]) > 1):
				# DOUBLE HEADER GAME ONE
				print('here')
				retval = 22
				game = game_array[0][0]
				game_id = game.game_id

				if (today.month < 10):
					if (today.day < 10):
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_0" + str(today.month) + "/day_0" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"
					else:
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_0" + str(today.month) + "/day_" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"
				else:
					if (today.day < 10):
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_" + str(today.month) + "/day_0" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"
					else:
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_" + str(today.month) + "/day_" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"

				tree = etree.fromstring(requests.get(url).text)

				if (game.home_team == 'Yankees'):
					batting_stats = tree.findall('batting')[0]
				else:
					batting_stats = tree.findall('batting')[1]

				for batter in batting_stats:
					if (batter.get('id') == '592450'):
						print('here')
						if (int(batter.get('hr')) == 0):
							print(game.game_status)
							if game.game_status == 'FINAL':
								# If the game is over, treat it as such
								#   self.lastGameVal = 0
								retval = 0
							else:
								# If the game is not over, treat it as if there has been no game yet today
								retval = 999
						else:
							# If he's homered, we don't care if the game is over
							#   self.lastGameVal = batter.get('hr')
							#   self.lastHRDate = today
							retval = int(batter.get('hr'))
				if game.game_status == 'FINAL':
					# If Judge isn't in batting_stats, but the game is over, treat it as such
					# self.lastGameVal = 0
					retval = 0
				else:
					# If Judge isn't in batting_stats, but the game is not over, treat it as if there has been no game yet today
					retval = 999

				# DOUBLE HEADER GAME TWO
				retval2 = 22
				game = game_array[0][1]
				game_id = game.game_id

				if (today.month < 10):
					if (today.day < 10):
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_0" + str(today.month) + "/day_0" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"
					else:
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_0" + str(today.month) + "/day_" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"
				else:
					if (today.day < 10):
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_" + str(today.month) + "/day_0" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"
					else:
						url = "http://gd2.mlb.com/components/game/mlb/year_" + str(today.year) + "/month_" + str(today.month) + "/day_" + str(today.day) + "/gid_" + game_id + "/boxscore.xml"

				tree = etree.fromstring(requests.get(url).text)

				if (game.home_team == 'Yankees'):
					batting_stats = tree.findall('batting')[0]
				else:
					batting_stats = tree.findall('batting')[1]

				print("batter", batter)
				for batter in batting_stats:
					if (batter.get('id') == '592450'):
						print('here')
						if (int(batter.get('hr')) == 0):
							if game.game_status == 'FINAL':
								# If the game is over, treat it as such
								# self.lastGameVal = 0
								retval2 = 0
							else:
								# If the game is not over, treat it as if there has been no game yet today
								retval2 = 999
						else:
							# If he's homered, we don't care if the game is over
							# self.lastGameVal = batter.get('hr')
							# self.lastHRDate = today
							print('this', int(batter.get('hr')))
							retval2 = int(batter.get('hr'))


				# Double header evaluation
				print('aaaa')
				print(retval)
				print(retval2)
				if retval > 0 and retval != 999 and retval != 22:
					print('hmm')
					self.lastGameVal = retval
					self.lastHRDate = today
					return retval
				if retval2 > 0 and retval2 != 999 and retval2 != 22:
					print('hmmmm')
					self.lastGameVal = retval2
					self.lastHRDate = today
					return retval2
				if retval2 == 999 or retval == 999:
					return 999
				else:
					print('this1')
					return 0

		# No game yet today
		else:
			print('this')
			return 999