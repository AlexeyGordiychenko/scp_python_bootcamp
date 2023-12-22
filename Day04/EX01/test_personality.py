from personality import turrets_generator


def check_sum(turret):
    assert (turret.neuroticism
            + turret.openness
            + turret.conscientiousness
            + turret.extraversion
            + turret.agreeableness) == 100


def check_output(turret, capfd):
    turret.shoot()
    turret.talk()
    turret.search()
    output = capfd.readouterr()
    assert output.out == "Shooting\nTalking\nSearching\n"


def test_1(capfd):
    turrets = turrets_generator()
    for _ in range(100):
        turret = next(turrets)
        check_sum(turret)
        check_output(turret, capfd)
