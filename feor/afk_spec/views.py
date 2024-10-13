import datetime
from pyplanet.views.generics.widget import WidgetView
import asyncio


class AFKWidget(WidgetView):
    widget_x = -999
    widget_y = -999
    template_name = 'afk_spec/AFK.xml'

    def __init__(self, app):
        super().__init__(self)
        self.app = app
        self.manager = app.context.ui
        self.id = 'pyplanet__AFK__Handling'
        self.subscribe("Player_AFK", self.handle_player_afk)
        
    
    async def get_context_data(self):
        context = await super().get_context_data()
        self.afk_timeout = await self.app.setting_afk_timeout.get_value()
        self.afk_timeout_check_frequency = await self.app.setting_afk_timeout_check_frequency.get_value()
        self.afk_timeout_wait = await self.app.setting_afk_timeout_wait.get_value()
        context.update({'afktimeout': self.afk_timeout,
                        'afktimeoutcheckfrequency': self.afk_timeout_check_frequency,
                        'afktimeoutwait': self.afk_timeout_wait,
                        })
        return context
    
    async def handle_player_afk(self, player, action, values, *args, **kwargs):
        await self.app.instance.gbx('ForceSpectator', player.login, 3)
        afk_message = await self.app.setting_afk_message.get_value()
        if await self.app.setting_afk_message_display.get_value():
            await self.app.instance.chat(afk_message.format(nickname=player.nickname))
