def scene_rock(engine):

    engine.pars.color("red", 100)

    engine.tmh13.color("white")
    engine.tmh13.sweep(
        speed="fast"
    )

    engine.tetra.fireball("red")
    engine.tetra.laser("redgreen")

    engine.strobe(
        fixtures=["pars"],
        speed=80
    )