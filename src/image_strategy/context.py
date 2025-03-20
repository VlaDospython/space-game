class Context:
    def set_strategy(self, strat):
        self.strategy = strat

    def get_surface(self):
        return self.strategy.get_surface()
