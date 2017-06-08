import random
import numpy as np
import matplotlib.pyplot as plt


from classes import Student, School



def create_students(num_students, num_schools):
	students = []
	for id_num in xrange(num_students):
		student = Student()
		student.id = id_num
		student.add_random_preferences(num_schools)
		students.append(student)
	return  students



def create_schools(num_students, num_schools, capacity, STB, walkzone):
	schools = []

	stb_preferences = [i for i in range(0,num_students)]
	random.shuffle(stb_preferences)
	for id_num in xrange(num_schools):
		school = School(capacity)
		school.id = id_num
		if STB:
			school.add_stb_preferences(stb_preferences, num_students, walkzone)
		else:
			school.add_mtb_preferences(num_students, walkzone)
		schools.append(school)

	return schools


def run_one_round(students, schools):
	for student in students: # proposals
		if student.rejected:
			school_id = student.preference_list[student.num_rejections]
			student.assignment = school_id
			schools[school_id].proposals.add(student.id)


	num_rejections = 0
	for school in schools: # rejctions
		if len(school.proposals) > school.capacity:
			num_rejections += school.reject_proposals(students)

	return num_rejections

def run_STB(q, n, m, walkzone):
	STB = True
	students = create_students(n, m)
	schools = create_schools(n, m, q, STB, walkzone)
	num_rejections = 1
	while num_rejections > 0:
		num_rejections = run_one_round(students, schools)

	rank_sum = 0.0
	ranks = [0 for i in schools]

	for student in students:
		ranks[student.num_rejections] += 1
		rank_sum += student.num_rejections
	avg_rank = rank_sum / float(n)
	ranks = np.cumsum([i / float(n) for i in ranks])
	print "STB", avg_rank, ranks
	return ranks


def run_MTB(q, n, m, walkzone):
	STB = False
	students = create_students(n, m)
	schools = create_schools(n, m, q, STB, walkzone)
	num_rejections = 1
	while num_rejections > 0:
		num_rejections = run_one_round(students, schools)

	#for school in schools:
		#print school.proposals

	rank_sum = 0.0

	ranks = [0 for i in schools]

	for student in students:
		ranks[student.num_rejections] += 1
		rank_sum += student.num_rejections
	avg_rank = rank_sum / float(n)
	ranks = np.cumsum([i / float(n) for i in ranks])
	print "MTB", avg_rank, ranks
	return ranks




def main():
	# variable names match paper https://web.stanford.edu/~iashlagi/papers/STBvsMTB.pdf
	m = 100 # number of schools
	n = 1000 # number of students
	q = n / m # capacity at all schools

	walkzone = False

	stb_ranks = run_STB(q, n, m, walkzone)
	mtb_ranks = run_MTB(q, n, m, walkzone)
	fig, ax = plt.subplots()
	line1, = ax.plot(range(0,25), mtb_ranks[0:25], label = "MTB, n = 10^3")
	line2, = ax.plot(range(0,25), stb_ranks[0:25], label = "STB, n = 10^3")


	m = 1000 # number of schools
	n = 10000 # number of students
	q = n / m # capacity at all schools

	walkzone = False

	stb_ranks = run_STB(q, n, m, walkzone)
	mtb_ranks = run_MTB(q, n, m, walkzone)
	line3, = ax.plot(range(0,25), mtb_ranks[0:25], label = "MTB, n = 10^4")
	line4, = ax.plot(range(0,25), stb_ranks[0:25], label = "STB, n = 10^4")

	ax.legend(loc='lower right')
	plt.show()


if __name__ == "__main__":
    main()
