import random

class Student:
	def __init__(self):
		self.id = -1
		self.assignment = None # school id number
		self.preference_list = [] # preferences over schools by id
		self.rejected = True # switch to true if rejected, false if tentatively accepted
		self.num_rejections = 0 # how many times student has been rejected

	def add_random_preferences(self, num_schools):
		self.preference_list = range(0,num_schools)
		random.shuffle(self.preference_list)
		#random.shuffle(self.preference_list)




class School:
	def __init__(self, q):
		self.proposals = set() # set of student ids who have proposed but haven't been rejected
		self.preference_list = [] # preferences over students
		self.id = -1 # number, equal to index in list of schools
		self.capacity = q # school capacity
		self.preference_map = {} # student_id --> preference rank

	def add_stb_preferences(self, preferences, num_students,walk_zone):
		self.preference_list = preferences
		self.map_preferences()
		if walk_zone:
			self.add_walkzone(num_students)

	def add_mtb_preferences(self, num_students, walk_zone):
		mtb_preferences = [i for i in range(0,num_students)]
		random.shuffle(mtb_preferences)
		self.preference_list = mtb_preferences
		self.map_preferences()
		if walk_zone:
			self.add_walkzone(num_students)

	def add_walkzone(self, num_students):
		# walkzone_range = id * capacity to (id - 1) * capacity 
		walkzone_range = range(self.id * self.capacity, (self.id - 1) * self.capacity )
		self.preference_map = {}
		walk_zone = []
		other = []
		for id_num in self.preference_list:
			if id_num in walkzone_range:
				walk_zone.append(id_num)
			else:
				other.append(id_num)
		self.preference_list = walk_zone + other
		self.map_preferences()

	def map_preferences(self):
		for rank, id_num in enumerate(self.preference_list):
			self.preference_map[id_num] = rank 

	# reject least preferred students, return number of rejections
	def reject_proposals(self, students): 
		orig_num_propsoals = len(self.proposals)
		if orig_num_propsoals <= self.capacity:
			return 0

		rank_idx, id_idx = 0, 1
		ranked_proposals = []
		for id_num in self.proposals:
			ranked_proposals.append((self.preference_map[id_num], id_num))

		ranked_proposals = sorted(ranked_proposals)

		for proposal in ranked_proposals[self.capacity:]:
			student_id = proposal[id_idx]
			self.proposals.remove(student_id)
			students[student_id].rejected = True
			students[student_id].num_rejections += 1

		return orig_num_propsoals - self.capacity


