package expensemanager.currency;

import java.util.EnumMap;
import java.util.Map;

public class FXService {
    private final Map<Currency, Double> rates = new EnumMap<>(Currency.class);

    public FXService() {
        rates.put(Currency.USD, 1.0);
        rates.put(Currency.EUR, 1.10); // 1 EUR = 1.10 USD
        rates.put(Currency.GBP, 1.30); // 1 GBP = 1.30 USD
        rates.put(Currency.CAD, 0.75); // 1 CAD = 0.75 USD
    }

    public Money convertToUsd(Money money) {
        if (money.getCurrency() == Currency.USD) {
            return money;
        }
        Double rate = rates.get(money.getCurrency());
        if (rate == null) {
            throw new IllegalArgumentException("Unsupported currency: " + money.getCurrency());
        }
        long convertedCents = (long) (money.getAmountCents() * rate);
        return new Money(convertedCents, Currency.USD);
    }
}
