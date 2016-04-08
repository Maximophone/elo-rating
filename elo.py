import pandas as pd
from datetime import datetime as dt

def update_elo_ratings(r_winner,r_loser,K=32):
	R0 = 10**(r_winner/400.)
	R1 = 10**(r_loser/400.)

	E0 = R0/(R0+R1)
	E1 = R1/(R0+R1)

	new_r_winner = r_winner + K*(1-E0)
	new_r_loser = r_loser - K*E1

	return new_r_winner, new_r_loser

class Ratings(object):
	def __init__(self,matches_url,players_url,initial_rating=500):
		self.initial_rating = initial_rating
		self.matches_url = matches_url
		self.players_url = players_url

	@property
	def matches(self):
	    return pd.read_csv(self.matches_url)

	@property
	def players(self):
	    return set(pd.read_csv(self.players_url).pname.unique())

	@property
	def ratings(self):
	    players_ratings = dict([(x,self.initial_rating) for x in self.players])
	    for _,row in self.matches.iterrows():
	    	players_ratings[row.pwin], players_ratings[row.plose] = update_elo_ratings(players_ratings[row.pwin], players_ratings[row.plose])
	    return players_ratings

	@property
	def ratings_string(self):
		rstring = []
		list_ratings = self.ratings.items()
		list_ratings.sort(key=lambda x:x[1],reverse=True)
		for i,(player,rating) in enumerate(list_ratings): rstring += ["%d. %10s : %d"%(i+1,player,rating)]
		return '\n'.join(rstring)

	@property
	def matches_string(self):
	    rstring = ["%20s %10s %10s"%("Date","Winner","Loser"),'']
	    for _,row in self.matches.iloc[::-1].iterrows():
	    	rstring += ["%20s %10s %10s"%(row.time,row.pwin,row.plose)]
	    return '\n'.join(rstring)
	
	def check_existing_player(self,pname):
		return pname in self.players

	def add_match(self,pwin,plose):
		if not self.check_existing_player(pwin) or not self.check_existing_player(plose): return False
		with open(self.matches_url,'a') as f:
			f.write("%s,%s,%s\n"%(pwin,plose,dt.now().strftime("%Y-%m-%d %H:%M:%S")))
		return True

	def add_player(self,pname):
		if self.check_existing_player(pname): return False
		with open(self.players_url,'a') as f:
			f.write("%s\n"%pname)
		return True
