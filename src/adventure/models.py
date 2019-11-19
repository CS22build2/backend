import json
from django.db import models
# from django.contrib.auth.models import User


class Room(models.Model):
    # Response Data
    room_id = models.IntegerField(default=0)
    title = models.TextField(default='DEFAULT TITLE')
    description = models.TextField(default='DEFAULT DESCRIPTION')
    coordinates = models.TextField(default='DEFAULT COORDINATES')
    players = models.CharField(defualt='[]')
    items = models.CharField(default='[]')
    exits = models.CharField(default='[]')
    cooldown = models.IntegerField(default=20)
    errors = models.CharField(default='[]')
    messages = models.CharField(default='[]')

    # "Unpacked" exits for connecting rooms/vertices
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)


    # https://stackoverflow.com/questions/22340258/django-list-field-in-model
    # Instead of using JSON and getters/setters, ManyToOne rels could be used
    def set_items(self, items):
        self.items = json.dumps(items)
        self.save()

    def get_items(self):
        return json.loads(self.items)

    def set_exits(self, exits):
        self.exits = json.dumps(exits)
        self.save()

    def get_exits(self):
        return json.loads(self.exits)

    def set_players(self, players):
        self.players = json.dumps(players)
        self.save()

    def get_players(self):
        return json.loads(self.players)

    def set_errors(self, errors):
        self.errors = json.dumps(errors)
        self.save()

    def get_errors(self):
        return json.loads(self.errors)

    def set_messages(self, messages):
        self.messages = json.dumps(messages)
        self.save()

    def get_messages(self):
        return json.loads(self.messages)

    # From CS Build Week 1
    def connect_rooms(self, destination_room, direction):
        destination_id = destination_room.id
        try:
            destination_room = Room.objects.get(id=destination_id)
        except Room.DoesNotExist:
            print('That room does not exist.')
        else:
            if direction == 'n':
                self.n_to = destination_id
            elif direction == 's':
                self.s_to = destination_id
            elif direction == 'e':
                self.e_to = destination_id
            elif direction == 'w':
                self.w_to = destination_id
            else:
                print('Invalid direction')
                return
            self.save()



class Player(models.Model):
    # Used in CS Build Week 1 (commented out):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # uuid = models.UUIDField(default=uuid.uuid4, uniqu=True)
    # current_room = models.IntegerField(default=0)
    name = models.TextField(default='DEFAULT PLAYER NAME')
    cooldown = models.IntegerField(default=20)
    encumbrance = models.IntegerField(default=0)
    strength = models.IntegerField(default=10)
    speed = models.IntegerField(default=10)
    gold = models.IntegerField(default=0)
    bodywear = models.TextField(default='NONE')
    footwear = models.TextField(default='NONE')
    inventory = models.CharField(default='[]')
    status = models.CharField(default='[]')
    errors = models.CharField(default='[]')
    messages = models.CharField(default='[]')


    def set_inventory(self, items):
        self.inventory = json.dumps(items)
        self.save()

    def get_inventory(self):
        return json.loads(self.inventory)

    def set_status(self, status):
        self.status = json.dumps(status)
        self.save()

    def get_status(self):
        return json.loads(self.status)

    def set_errors(self, errors):
        self.errors = json.dumps(errors)
        self.save()

    def get_errors(self):
        return json.loads(self.errors)

    def set_messages(self, messages):
        self.messages = json.dumps(messages)
        self.save()

    def get_messages(self):
        return json.loads(self.messages)

    def initialize(self):
        if self.current_room == 0:
            self.current_room = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.current_room)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()
    pass


# What is this code for?

# @receiver(post_save, sender=User)
# def create_user_player(sender, instance, created, **kwargs):
#     if created:
#         Player.objects.create(user=instance)
#         Token.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_player(sender, instance, **kwargs):
#     instance.player.save()