import torchvision
import torch
import numpy as np
import warnings
import torch.nn as nn
from typing import List
from ..optim.optimizer import Adam, SGD, Adamax, RMSProp, Adagrad

warnings.filterwarnings("ignore")


class Feed_Forward_Neural_Network(nn.Module):
    """
    The goal of this class is creating
    a basic neural network that will
    be used with the coded optimizer to
    check its working well

    Arguments:
        -None
    Returns:
        -None
    """

    def __init__(self):
        super(Feed_Forward_Neural_Network, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 10)

    def forward(self, x: torch.tensor) -> torch.tensor:
        """
        The goal of this function is
        to apply a forward pass operation
        to a given input data

        Arguments:
            -x: torch.tensor: The input
            data
        Returns:
            -output: torch.tensor: The
            transformed input data
        """

        x = x.view(-1, 28 * 28)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        output = self.fc3(x)

        return output


def get_label(x: int) -> torch.tensor:
    """
    The goal of this function
    is to generate fake labels
    for the try of the neural
    network on the MNIST dataset

    Arguments:
        -x: int: The number that's
        represented on a given image
    Returns:
        -labels: torch.tensor: The tensor
        containing binary position of the
        given number
    """
    labels = torch.zeros(size=(10,))
    labels[x] = 1
    return np.array(labels)


def load_mnist_data(batch_size: int = 128) -> torch._utils:
    """
    The goal of this function is to
    load the MNIST dataset to carry
    on experiments with Adam optimizer

    Arguments:
        -batch_size: int: The batch size
        associated with MNIST loading
    Returns:
        -data: torch.tensor: The MNIST
        data
    """

    train_loader = torch.utils.data.DataLoader(
        torchvision.datasets.MNIST(
            "data/",
            train=True,
            download=True,
            transform=torchvision.transforms.Compose(
                [torchvision.transforms.ToTensor()]
            ),
        ),
        batch_size=batch_size,
        shuffle=True,
    )

    return train_loader


def launch_training(
    optimizer: torch.optim = SGD, num_epochs: int = 10, lr: float = 1e-3
) -> None:
    """
    The goal of this function is to
    launch the training of the feed
    forward neural network on the MNIST
    dataset

    Arguments:
        -optimizer: torch.optim: The custom
        optimizer that will be used
    Returns:
        -None
    """

    assert optimizer in [
        SGD,
        Adam,
        Adamax,
        RMSProp,
        Adagrad,
    ], f"optimizer should be SGD or Adam, got {optimizer}"

    model = Feed_Forward_Neural_Network()
    criterion = nn.CrossEntropyLoss()
    optimizer = optimizer(model=model, params=model.parameters(), lr=lr)

    train_loader = load_mnist_data()
    n_total_steps = len(train_loader)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            images = images.reshape(-1, 28 * 28).to(device)
            labels = labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.zero_grad()
            optimizer.step()

            if (i + 1) % 100 == 0:
                print(
                    f"Epoch [{epoch+1}/{num_epochs}], "
                    f"Step[{i+1}/{n_total_steps}], "
                    f"Loss: {loss.item(): .4f}"
                )


def get_training_lossses(
    optimizer: torch.optim = SGD, num_epochs: int = 5, lr: float = 1e-5
) -> List:
    """
    The goal of this function is to
    store the losses of the optimizers
    at different steps
    """

    assert optimizer in [
        SGD,
        Adam,
        Adamax,
        RMSProp,
        Adagrad,
    ], f"optimizer should be SGD or Adam, got {optimizer}"

    losses = []
    model = Feed_Forward_Neural_Network()
    criterion = nn.CrossEntropyLoss()
    optimizer = optimizer(model=model, params=model.parameters(), lr=lr)

    train_loader = load_mnist_data()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            images = images.reshape(-1, 28 * 28).to(device)
            labels = labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            losses.append(loss.item())
            loss.backward()
            optimizer.zero_grad()
            optimizer.step()

    return losses
