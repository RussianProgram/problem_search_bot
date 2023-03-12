from models import Problem, Topic, create_session
from sqlalchemy.sql.expression import func
import random

def filter_by_topic(topic, problems):
    return [p for p in problems if topic in p.topics]

def get_random_problems(
    topic: str | None = None, 
    difficulty: int | None = None,
    limit: int = 10
):
    Session = create_session()
   
    with Session() as session:
        problems = session.query(Problem)
        # if diffuculty set, than filter by it
        if difficulty:
            problems = problems.filter(Problem.difficulty == difficulty).all()#.order_by(func.random())

        # fetch and limit
        #problems = problems.limit(limit).all()

        if topic:
            topic = session.query(Topic).filter(Topic.name == topic).one_or_none()
            problems = filter_by_topic(topic, problems)

        top_random_problems = []
        
        for _ in range(limit):
            try:
                p = random.choice(problems)
            except IndexError:
                break
            else:
                if p not in top_random_problems:
                    top_random_problems.append(p)
                    problems.remove(p)

        return top_random_problems
            

def get_problems(
    topic: str | None = None, 
    difficulty: int | None = None,
    start: int = 0,
    end: int = 10
    ):
    Session = create_session()
    with Session() as session:
        problems = session.query(Problem)
        # if diffuculty set, than filter by it
        if difficulty:
            problems = problems.filter(Problem.difficulty == difficulty)

        # fetch data slicing from start to end
        problems = problems.offset(start).limit(end - start).all()
        print(problems[0].topics)

        # if topic is set, than filter by it 
        if topic:
            topic = session.query(Topic).filter(Topic.name == topic).one_or_none()
            problems = filter_by_topic(topic, problems)

        return problems


def insert_data(problem_data: dict):
        Session = create_session()
        with Session() as session:
            problem = session.query(Problem).\
                filter(
                    Problem.name == problem_data['name'], 
                    Problem.number == problem_data['number']
                    ).one_or_none()

            if not problem:
                problem = Problem(
                    url=problem_data['url'],
                    name=problem_data['name'], 
                    number=problem_data['number'], 
                    difficulty=problem_data['difficulty'], 
                    solved_count=problem_data['solutions']
                    )
            
            for topic_name in problem_data['topics']:
                topic = session.query(Topic).filter(Topic.name == topic_name).one_or_none()
                
                if not topic:
                    topic = Topic(name=topic_name)
                    session.add(topic)
                
                problem.topics.append(topic)

            session.add(problem)     
            session.commit()

            
if __name__ == "__main__":
    a = get_random_problems(difficulty=800, topic="greedy", limit=10)
    print(a)