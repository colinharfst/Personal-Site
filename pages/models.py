from django.db import models
import datetime
import mlbgame
import xml.etree.cElementTree as etree
import requests

class Judge(models.Model):
	
	lastGameVal = models.IntegerField(default=-1)
	lastHRDate = models.DateTimeField('lastHRDate')

	def didJudgeHR(self):

		today = datetime.datetime.today() #datetime.datetime(2019, 4, 8, 20, 00)
		game_array = mlbgame.games(today.year, today.month, today.day, home='Yankees', away='Yankees')

		if game_array != []:
			if len(game_array) == 1:
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
					if (int(batter.get('hr')) == 0):
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
				# If Judge isn't in batting_stats, but the game is over, treat it as such
				self.lastGameVal = 0
				return 0
			else:
				# If Judge isn't in batting_stats, but the game is not over, treat it as if there has been no game yet today
				return 999

		# DOUBLE HEADER MEANS DOUBLE CODDDDDDDDDEEEEEEEEE
		if (len(game_array[0]) > 1):
			# DOUBLE HEADER GAME ONE
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
					if (int(batter.get('hr')) == 0):
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

			for batter in batting_stats:
				if (batter.get('id') == '592450'):
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
						retval2 = int(batter.get('hr'))
			if game.game_status == 'FINAL':
				# If Judge isn't in batting_stats, but the game is over, treat it as such
				# self.lastGameVal = 0
				retval2 = 0
			else:
				# If Judge isn't in batting_stats, but the game is not over, treat it as if there has been no game yet today
				retval2 = 999

			# Double header evaluation
			if retval > 0 and retval != 999 and retval != 22:
				self.lastGameVal = retval
				self.lastHRDate = today
			if retval2 > 0 and retval2 != 999 and retval2 != 22:
				self.lastGameVal = retval2
				self.lastHRDate = today
			if retval2 == 999 or retval == 999:
				return 999
			else:
				return 0

		# No game yet today
		else:
			return 999