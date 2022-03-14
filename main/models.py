from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404


class User(AbstractUser):
    status = models.CharField(max_length=255)

    def get_all_vote_facts(self):
        return VoteFact.objects.filter(author=self)

    def get_all_voted_variants(self):
        return [fact.variant for fact in self.get_all_vote_facts()]


class UserSettings(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)


class Voting(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now=True)

    def user_has_already_voted(self, user):
        facts = VoteFact.objects.filter(user=user)
        for fact in facts:
            for fact_variant in fact.votefactvariant_set.all():
                if fact_variant.variant.voting == self:
                    return True
        return False

    def make_votefact(self, author, variant_ids_list):
        if len(variant_ids_list) == 0:
            raise PermissionError('Список вариантов для голосования пуст')

        if self.user_has_already_voted(author):
            raise PermissionError('Пользователь уже оставлял свой голос в текущем голосовании')

        for variant_id in variant_ids_list:
            variant = get_object_or_404(VoteVariant,  id=variant_id)
            if variant.voting != self:
                raise PermissionError('Нельзя голосоваать за варианты, не привязанные к текущему голосованию')

        fact = VoteFact(user=author)
        fact.save()

        for variant_id in variant_ids_list:
            variant = get_object_or_404(VoteVariant, id=variant_id)
            record = VoteFactVariant(fact=fact, variant=variant)
            record.save()


class VoteVariant(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)


class VoteFact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)


class VoteFactVariant(models.Model):
    fact = models.ForeignKey(to=VoteFact, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=VoteVariant, on_delete=models.CASCADE)
