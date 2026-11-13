"""The two-moons dataset used throughout the chapter."""
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def load(top=np.pi):
    # 80 points, 70% training, features rescaled to [0, top]
    X, y = make_moons(n_samples=80, noise=0.2, random_state=3)
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.3, random_state=3, stratify=y)
    scaler = MinMaxScaler((0, top)).fit(Xtr)   # fit on train only
    return scaler.transform(Xtr), scaler.transform(Xte), ytr, yte

if __name__ == "__main__":
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC
    Xtr, Xte, ytr, yte = load()
    print("training set:", Xtr.shape, " test set:", Xte.shape)
    print("class counts (train):", np.bincount(ytr))
    for name, model in [("logistic regression",
                         LogisticRegression()),
                        ("SVM, Gaussian kernel", SVC())]:
        model.fit(Xtr, ytr)
        print(f"{name:22s} train {model.score(Xtr, ytr):.3f}"
              f"  test {model.score(Xte, yte):.3f}")
    # Plotting code for Figure 16.1: see the companion repository.
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 3.6))
    for c, col in [(0, "#1F5FBF"), (1, "#F28C28")]:
        ax.scatter(*Xtr[ytr == c].T, color=col, label=f"train, y={c}")
        ax.scatter(*Xte[yte == c].T, color=col, marker="x",
                   label=f"test, y={c}")
    ax.set_xlabel("feature $x_0$")
    ax.set_ylabel("feature $x_1$")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig("figures/ch16/moons.pdf")
