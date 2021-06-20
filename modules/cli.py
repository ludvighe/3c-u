import secrets
import pandas as pd

from modules.util.cli_tools import CliTools
import shrimpy_api.shrimpy_api as shrimpy
import modules.util.settings as settings
import modules.util.email as email


class Cli:
    def __init__(self) -> None:
        self.cli = CliTools()
        self.alerts = []
        while True:
            self.main_menu()

    # def test_menu(self):
    #     pass

    def quit(self):
        if self.cli.yes_no('Are you sure you want to quit?\nNote: This will not cancel any ongoing alerts.'):
            print('Quitting 3c-u')
            exit()

    # MAIN MENU
    def main_menu(self):
        menu_dict = {
            # 'test': self.test_menu,
            'Tickers': self.tickers_menu,
            'Alerts': self.alerts_menu,
            'Quit': self.quit
        }
        options = list(menu_dict.keys())
        option = self.cli.menu('Main menu', options)
        menu_dict[
            options[
                option if option != -1
                else options.index('Quit')
            ]
        ]()

    # TICKERS
    def tickers_menu(self):
        print('Loading market data...')
        df = pd.DataFrame(shrimpy.fetch_market_data(
            exchange=settings.settings['exchange']))

        view_tokens = self.cli.yes_no(
            'View all available tickers on exchange [' + settings.settings['exchange'] + ']?')
        if view_tokens:
            print(df.set_index('symbol').sort_index().to_markdown())

        while True:
            ticker = self.cli.menu(
                title='Tickers (please enter currency symbol)',
                options=df['name'].to_list(),
                index=df['symbol'].to_list(),
                quiet=True
            )
            if ticker != -1:
                token = df[df['symbol'] == ticker]
                print(token.set_index('symbol').sort_index().to_markdown())
            if ticker == -1:
                break

    # ALERTS
    def alerts_menu(self):
        menu_dict = {
            'List alerts': self.list_alerts,
            'Set alert': self.set_alert
        }
        options = list(menu_dict.keys())
        while True:
            option = self.cli.menu('Alerts', options)
            if option == -1:
                break
            else:
                menu_dict[options[option]]()

    def list_alerts(self):
        if len(self.alerts) <= 0:
            print('\nNo alerts set')
        else:
            print('\nNote: Finished alerts will also be displayed.')
            self.cli.list_print(self.alerts)

    def set_alert(self):

        # Token selection
        token = self.cli.quiestion('\nToken to watch (enter symbol): ')
        if token == -1:
            return
        token = token.upper()

        print('Checking token availability...')
        tickers = pd.DataFrame(shrimpy.fetch_market_data(
            exchange=settings.settings['exchange']))
        if token in tickers['symbol'].to_list():
            print('Selected:\n' +
                  tickers[tickers['symbol'] == token].set_index('symbol').to_markdown())
        else:
            if self.cli.yes_no('Token does not exist. See available tokens?'):
                self.cli.list_print(tickers['symbol'].to_list())
            return

        # Select if price is to exceed of fall below threshold
        options = ['exceeds a price', 'falls below a price']
        exceed_fall = self.cli.menu('Alert when token', options)
        if exceed_fall == -1:
            return

        try:
            # Threshold entry
            threshold = float(self.cli.quiestion(
                '\nThreshold for alert ($USD): '))
            if threshold == -1:
                return

            # Interval entry: At which rate boolfunc will repeat
            interval = self.cli.quiestion(
                '\nHow many minutes between each check? (default: 10): ')
            if interval == -1:
                return
            if interval == '':
                interval = 10
            else:
                interval = int(interval)

            # Confirmation of alert configuration
            if self.cli.yes_no(
                    f'So this alert should send an email to {secrets.TO_EMAIL_ADDRESS}\n- when {token} {options[exceed_fall]} of ${threshold} USD\n- and check if it has every {interval} minutes?\n'):

                # Function to run in alert loop
                def boolfunc():
                    tickers = pd.DataFrame(shrimpy.fetch_market_data(
                        settings.settings['exchange']))
                    price = float(tickers[tickers['symbol'] ==
                                          token]['priceUsd'].values[0])

                    print(f'Current price: {price}\tThreshold: {threshold}')
                    if exceed_fall == 0 and price >= threshold:
                        return True
                    elif exceed_fall == 1 and price <= threshold:
                        return True
                    else:
                        return False

                subject = f'3c-u Alert: {token} has ' + 'exceeded' * (
                    exceed_fall == 0) + 'fallen below' * (exceed_fall == 1) + ' threshold'
                body = f'Hello!\nAllan here. Just wanted to tell you that an alert has gone off.\n\n{token} has ' + 'exceeded' * (
                    exceed_fall == 0) + 'fallen below' * (exceed_fall == 1) + f' ${threshold} USD as of now.'
                name = f'{token} ' + 'exceeds' * (
                    exceed_fall == 0) + 'falls below' * (exceed_fall == 1) + f' {threshold}'
                alert = email.start_alerter(
                    subject=subject,
                    body=body,
                    boolfunc=boolfunc,
                    name=name
                )
                print('Alert set!')
                self.alerts.append(alert.getName())
                alert.start()
            else:
                print('Cancelling alert.')
        except ValueError:
            print('Invalid input. Cancelling alert configuration.\n')
