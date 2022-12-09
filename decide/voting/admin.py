from django.contrib import admin
from django.utils import timezone

from .models import QuestionOption
from .models import Question
from .models import Voting
from .bot import BotTelegram
from .views import BotMessageHandler
from base import mods
from .filters import StartedFilter


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()
        try:
            bot_message = BotMessageHandler.create_bot_message_start(str(v.id))
            BotTelegram.botSendMessage(bot_message)
        except:
            pass


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')

        # Bot
        voting_for_bot = mods.get('voting', params={'id': v.id})
        bot_message = BotMessageHandler.create_bot_message_tally(
            voting_for_bot)
        BotTelegram.botSendMessage(bot_message)
        # end Bot

        v.tally_votes(token)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [start, stop, tally]


admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
