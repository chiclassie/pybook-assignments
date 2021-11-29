import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    age = []
    current_date = dt.date.today()
    friends = get_friends(user_id, fields=["bdate"]).items
    for friend in friends:
        try:
            birthday_date = dt.datetime.strptime(friend["bdate"], "%d.%m.%Y")  # type: ignore
        except (KeyError, ValueError):
            continue
        age.append(
            current_date.year
            - birthday_date.year
            - (
                current_date.month < birthday_date.month
                or (
                    current_date.month == birthday_date.month
                    and current_date.day < birthday_date.day
                )
            )
        )

    if age:
        return statistics.median(age)
    return None
