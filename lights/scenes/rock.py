def scene_rock(engine):
    engine.set_color("pars", "red", 100)

    moving_head = engine.fixture("moving_head")
    moving_head.set_color("white")
    moving_head.sweep(200)

    tetra = engine.fixture("tetra")
    tetra.fireball("red")
    tetra.laser("redgreen")
