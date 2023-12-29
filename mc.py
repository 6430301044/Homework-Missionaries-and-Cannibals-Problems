class MissionariesAndCannibalsProble:
    def __init__(self, initial_state, parent=None, action=None):
        self.state = initial_state
        self.parent = parent
        self.action = action

    def is_valid(self, state):
        missionaries_left, cannibals_left, boat, missionaries_right, cannibals_right = state

        # ตรวจสอบจำนวนนักบวช ว่าค่าที่ใส่มาไม่ติดลบ เพื่อป้องกัน input ที่ติดลบ ถ้าเป็นจริงให้คืนค่า false
        if missionaries_left < 0 or missionaries_right < 0:
            return False

        # ตรวจสอบว่าจำนวนมนุษย์กินคน ค่าที่ใส่มาไม่ติดลบ เพื่อป้องกัน input ที่ติดลบ ถ้าเป็นจริงให้คืนค่า false
        if cannibals_left < 0 or cannibals_right < 0:
            return False

        # ตรวจสอบว่าจำนวนนักบวชมากกว่าหรือเท่ากับ มนุษย์กินคนไหม ถ้าเป็นจริงให้คืนค่า false ทั้งซ้ายและขวา
        if missionaries_left > 0 and missionaries_left < cannibals_left:
            return False

        if missionaries_right > 0 and missionaries_right < cannibals_right:
            return False

        if boat == 1 and (missionaries_left + cannibals_left == 0):
            return False
    
        # ตรวจสอบสถานะของเรือ ถ้าไม่ใช่ค่า 0 และ 1 ให้คืนค่า false
        if boat not in (0, 1):
            return False

        return True

    def goal_test(self, state):
        #(นักบวชฝั่งซ้าย, มนุษย์กินคนฝั่งซ้าย, สถานะเรือ, นักบวชฝั่งขวา, มนุษย์กินคนฝั่งขวา)
        # สถานะเรือ = 1 อยู่ฝั่งซ้ายจะไปฝั่งขวา, = 0 อยู่ฝั่งขวาจะไปฝั่งซ้าย
        # initial state กับ goal test ต้องสัมพันธ์กันไม่งั้นหา solution ไม่ได้ และ initial stat มนุษย์กินคนห้ามมากกว่านักบวชไม่งั้นหา solution ไม่ได้ 
        return state == (0, 0, 0, 3, 3)

    def get_successors(self, state):
        successors = []

        #รูปแบบ action ทั้งหมดที่เป็นไปได้ (m, c, b)
        if state.state[2] == 1:  # Check if the boat is on the right
            actions = [(1, 0, 1), (2, 0, 1), (0, 1, 1), (0, 2, 1), (1, 1, 1)]
        else:
            actions = [(-1, 0, 0), (-2, 0, 0), (0, -1, 0), (0, -2, 0), (-1, -1, 0)]

        missionaries_left, cannibals_left, boat, missionaries_right, cannibals_right = state.state

        # Iterate through possible actions
        for action in actions:
            delta_m, delta_c, delta_b = action

            # Determine the new state
            new_state = (
                missionaries_left - delta_m,
                cannibals_left - delta_c,
                1 - boat,
                missionaries_right + delta_m,
                cannibals_right + delta_c,
            )

            # Check if the new state is valid
            if self.is_valid(new_state):
                # Create a new MissionariesAndCannibalsProble object for the new state
                new_problem = MissionariesAndCannibalsProble(new_state, parent=state, action=action)
                successors.append((new_problem, action))

        return successors

def print_solution(path):
    for t in path:
        print(f"Left: {t.state[:2]}, Boat: {t.state[2]}, Right: {t.state[3:]} ")

def breadth_first_search(problem):
    frontier = [problem]
    explored = set()

    while frontier:
        state = frontier.pop(0)
        if problem.goal_test(state.state):
            path = []
            while state:
                path.append(state)
                state = state.parent
            path.reverse()
            print_solution(path)
            return True

        explored.add(state)
        for successor, action in problem.get_successors(state):
            if successor not in explored or successor not in frontier:
                frontier.append(successor)

    return False

# สร้างปัญหา Missionaries and Cannibals
# อย่าลืมตั้ง goal test ให้ match กับ initial_state
initial_state = (3, 3, 1, 0, 0)
problem = MissionariesAndCannibalsProble(initial_state)

#(นักบวชฝั่งซ้าย, มนุษย์กินคนฝั่งซ้าย, สถานะเรือ,นักบวชฝั่งขวา, มนุษย์กินคนฝั่งขวา)
# สถานะเรือ = 1 อยู่ฝั่งซ้ายจะไปฝั่งขวา, = 0 อยู่ฝั่งขวาจะไปฝั่งซ้าย 

#ตัวอย่างโจทย์
#initial_state = (5, 4, 1, 0, 0) , goal_test = (0, 0, 0, 5, 4)
#initial_state = (4, 4, 1, 0, 0) , goal_test = (0, 0, 0, 4, 4)

# แก้ปัญหาด้วยวิธี Breadth-First Search
result = breadth_first_search(problem)

if not result:
    print("No solution found.")

