package expensemanager.currency;

import java.util.Objects;

public class Money implements Comparable<Money> {
    private final long amountCents;
    private final Currency currency;

    public Money(long amountCents) {
        this(amountCents, Currency.USD);
    }

    public Money(long amountCents, Currency currency) {
        this.amountCents = amountCents;
        this.currency = currency != null ? currency : Currency.USD;
    }

    public long getAmountCents() {
        return amountCents;
    }

    public Currency getCurrency() {
        return currency;
    }

    private void checkCurrency(Money other) {
        if (this.currency != other.currency) {
            throw new IllegalArgumentException(
                "Cannot compare money across currencies without conversion: " +
                this.currency + " vs " + other.currency
            );
        }
    }

    @Override
    public int compareTo(Money other) {
        checkCurrency(other);
        return Long.compare(this.amountCents, other.amountCents);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Money)) return false;
        Money money = (Money) o;
        return amountCents == money.amountCents && currency == money.currency;
    }

    @Override
    public int hashCode() {
        return Objects.hash(amountCents, currency);
    }

    @Override
    public String toString() {
        return amountCents + " " + currency;
    }
}

