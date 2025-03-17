def is_colliding_rect(rect1, rect2):
    if hasattr(rect1, "rect"):
        rect1 = rect1.rect
    if hasattr(rect2, "rect"):
        rect2 = rect2.rect

    buffer = 10  # pixel buffer for collision

    if rect1.right < rect2.left + buffer:
        return False
    if rect1.left > rect2.right - buffer:
        return False
    if rect1.bottom > rect2.top - buffer:
        return False
    if rect1.top < rect2.bottom + buffer:
        return False
    return True


def is_colliding_fruit(Player, Fruit):
    buffer = 4  # pixel buffer for collision

    if Player.rect.right < Fruit.rect.left + buffer:
        return False
    if Player.rect.left > Fruit.rect.right - buffer:
        return False
    if Player.rect.bottom > Fruit.rect.top - buffer:
        return False
    if Player.rect.top < Fruit.rect.bottom + buffer:
        return False
    return True


def is_colliding_walls(player, walls):
    for wall in walls:
        if (
            player.rect.right > wall.rect.left
            and player.rect.left < wall.rect.right
            and player.rect.bottom < wall.rect.top
            and player.rect.top > wall.rect.bottom
        ):
            wall.color = (1, 0, 0)
            return True
        else:
            wall.color = (1, 1, 1)
    return False
