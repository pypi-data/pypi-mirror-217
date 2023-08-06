#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2023 Théo Morales <theo.morales.fr@gmail.com>
#
# Distributed under terms of the MIT license.

"""
MAML example on the Omniglot dataset using MetaBatch.
"""


import numpy as np
import higher
import argparse
import random
import torchvision
import torch
from tqdm import tqdm
import sys
import os

from typing import List, Tuple

from torch import nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class ConvNetClassifier(nn.Module):
    def __init__(self, device, input_channels: int, n_classes: int):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(input_channels, 64, 3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )
        self.flc = nn.Sequential(
            nn.Linear(64 * 20 * 20, n_classes)
        ).to(device)

    def forward(self, x):
        x = self.cnn(x)
        x = x.view(x.size(0), -1)
        x = self.flc(x)
        return x

class OmniglotDataset:
    def __init__(
        self,
        meta_batch_size: int,
        img_size: int,
        k_shot: int,
        k_query: int,
        n_way: int,
        evaluation: bool = False,
    ):
        assert (
            k_shot + k_query
        ) <= 20, "Not enough samples per class for these k-shot and k-query values!"
        self.idx = 0
        self.k_shot = k_shot
        self.k_query = k_query
        self.n_way = n_way
        self.eval = evaluation
        self.img_size = img_size
        self.meta_batch_size = meta_batch_size
        path = os.path.join("datasets", "omniglot.npy")
        if os.path.exists(path) and device == "cpu":
            print("[*] Loading Omniglot from a saved file...")
            self.dataset = np.load(path)
        else:
            print("[*] Loading and preparing Omniglot...")
            self.dataset = self._load(not evaluation, img_size)
            if device == "cpu":
                np.save(path, self.dataset)
        self._cache = self._load_in_cache()

    def _load(self, background, img_size):
        dataset = torchvision.datasets.Omniglot(
            root="./datasets/",
            download=True,
            background=background,
            transform=torchvision.transforms.Compose(
                [
                    lambda x: x.convert("L"),
                    lambda x: x.resize((img_size, img_size)),
                    lambda x: np.reshape(x, (img_size, img_size, 1)),
                    lambda x: np.transpose(x, [2, 0, 1]),
                    lambda x: x / 255.0,
                ]
            ),
        )
        tmp = dict()
        data = []
        t = tqdm(total=len(dataset))
        for x, y in dataset:
            if y not in tmp:
                tmp[y] = []
            tmp[y].append(x)
            t.update()
        for y, x in tmp.items():
            data.append(np.array(x, dtype=np.float32))
            t.update()
        data = torch.tensor(data, device=device)
        del tmp
        t.close()
        return data

    def _load_in_cache(self, batch_size=100):
        cache = SimpleQueue()
        for _ in range(batch_size):
            batch = []
            for i in range(self.meta_batch_size):
                classes = (
                    np.random.choice(self.dataset.shape[0], self.n_way, False)
                    if not self.eval
                    else list(
                        range(
                            self.idx, min(self.dataset.shape[0], self.idx + self.n_way)
                        )
                    )
                )
                if self.eval and not classes:
                    cache.put([])
                    return cache
                x_spt, y_spt, x_qry, y_qry = [], [], [], []
                for j, class_ in enumerate(classes):
                    samples = (
                        np.random.choice(
                            self.dataset.shape[1], self.k_shot + self.k_query, False
                        )
                        if not self.eval
                        else list(range(self.k_shot + self.k_query))
                    )
                    x_spt.append(self.dataset[class_][samples[: self.k_shot]])
                    y_spt.append(torch.tensor([j] * self.k_shot, device=device))
                    x_qry.append(self.dataset[class_][samples[self.k_shot :]])
                    y_qry.append(torch.tensor([j] * self.k_query, device=device))

                # Shuffle the batch
                spt_sz, qry_sz = len(classes) * self.k_shot, len(classes) * self.k_query
                perm = torch.randperm(spt_sz)
                x_spt = torch.stack(x_spt, dim=0).reshape(
                    spt_sz, 1, self.img_size, self.img_size
                )[perm]
                y_spt = torch.stack(y_spt, dim=0).reshape(spt_sz)[perm]
                perm = torch.randperm(qry_sz)
                x_qry = torch.stack(x_qry, dim=0).reshape(
                    qry_sz, 1, self.img_size, self.img_size
                )[perm]
                y_qry = torch.stack(y_qry, dim=0).reshape(qry_sz)[perm]

                spt_loader = DataLoader(
                    list(zip(x_spt, y_spt)),
                    batch_size=self.k_shot,
                    shuffle=False,
                    pin_memory=False,
                )
                qry_loader = DataLoader(
                    list(zip(x_qry, y_qry)),
                    batch_size=self.k_query,
                    shuffle=False,
                    pin_memory=False,
                )
                batch.append((spt_loader, qry_loader))
                if self.eval:
                    self.idx += self.n_way
            cache.put(batch)  # Should not need exception handling
        return cache

    def __iter__(self):
        self.idx = 0
        return self

    @property
    def total_batches(self):
        return self.dataset.shape[0] // self.n_way // self.meta_batch_size + 1

    def __next__(self):
        """
        Build a batch of N (for N-way classification) tasks, where each task is a random class.
        """
        if self._cache.empty():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
            self._cache = self._load_in_cache()
        batch = self._cache.get()
        return batch

    def __len__(self):
        return self.total_batches * self.meta_batch_size



class MAML(torch.nn.Module):
    def __init__(
        self,
        learner: torch.nn.Module,
        meta_lr=1e-4,
        inner_lr=1e-3,
        steps=1,
        loss_function=torch.nn.MSELoss(reduction="sum"),
    ):
        super().__init__()
        self.meta_lr = meta_lr  # This term is beta in the paper
        # TODO: Make the inner learning rate optionally learnable
        self.inner_lr = inner_lr  # This term is alpha in the paper
        self.learner = learner
        self.inner_steps = steps
        self.meta_opt = torch.optim.Adam(self.learner.parameters(), lr=self.meta_lr)
        self.inner_opt = torch.optim.SGD(self.learner.parameters(), lr=self.inner_lr)
        self.inner_loss = loss_function
        self.meta_loss = loss_function
        self._compute_accuracy = type(self.inner_loss) is torch.nn.CrossEntropyLoss

    def train_on_batch(self, tasks_batch):
        # sprt should never intersect with qry! So only shuffle the task
        # at creation!
        # For each task in the batch
        inner_losses, meta_losses, accuracies = [], [], []
        self.meta_opt.zero_grad()
        for i, task in enumerate(tasks_batch):
            with higher.innerloop_ctx(
                self.learner, self.inner_opt, copy_initial_weights=False
            ) as (f_learner, diff_opt):
                meta_loss, inner_loss, task_accuracies = 0, 0, []
                sprt, qry = task
                f_learner.train()
                for s in range(self.inner_steps):
                    step_loss = 0
                    for x, y in sprt:
                        # sprt is an iterator returning batches
                        y_pred = f_learner(x)
                        step_loss += self.inner_loss(y_pred, y)
                    inner_loss += step_loss.detach()
                    diff_opt.step(step_loss)

                f_learner.eval()
                for x, y in qry:
                    y_pred = f_learner(x)  # Use the updated model for that task
                    # Accumulate the loss over all tasks in the meta-testing set
                    meta_loss += self.meta_loss(y_pred, y)
                    if self._compute_accuracy:
                        scores, indices = y_pred.max(dim=1)
                        acc = (y == indices).sum() / y.size(
                            0
                        )  # Mean accuracy per batch
                        task_accuracies.append(acc)

                # Divide by the number of samples because reduction is set to 'sum' so that
                # the meta-objective can be computed correctly.
                meta_losses.append(
                    meta_loss.detach().div_(self.inner_steps * len(sprt.dataset))
                )
                inner_losses.append(inner_loss.mean().div_(len(qry.dataset)))
                if self._compute_accuracy:
                    accuracies.append(torch.tensor(task_accuracies).mean())

                # Update the model's meta-parameters to optimize the query
                # losses across all of the tasks sampled in this batch.
                # This unrolls through the gradient steps.
                meta_loss.backward()

        self.meta_opt.step()
        avg_inner_loss = torch.tensor(inner_losses).mean().item()
        avg_meta_loss = torch.tensor(meta_losses).mean().item()
        avg_accuracy = torch.tensor(accuracies).mean().item()
        return avg_inner_loss, avg_meta_loss, avg_accuracy

    def eval_task_batch(self, task_batch):
        """
        Use the Higher innerloop context to evaluate a task batch.
        Not suited for inference, only for evaluation.
        """
        batch_loss = []  # Average loss of the batch of tasks
        for task in task_batch:
            with higher.innerloop_ctx(self.learner, self.inner_opt) as (
                f_learner,
                diff_opt,
            ):
                qry_loss = 0
                sprt, qry = task
                f_learner.train()
                for s in range(self.inner_steps):
                    step_loss = 0
                    for x, y in sprt:
                        y_pred = f_learner(x)
                        step_loss += self.inner_loss(y_pred, y)
                    diff_opt.step(step_loss)

                f_learner.eval()
                for x, y in qry:
                    y_pred = f_learner(x)
                    qry_loss += self.inner_loss(y_pred, y)
                batch_loss.append(qry_loss.detach().div_(len(qry.dataset)))
        return torch.tensor(batch_loss).mean()

    def adapt(self, task_support):
        """
        Adapt the model to the task using the support set. This is typically used for inference on
        a novel task.
        """
        self.learner.train()
        for s in range(self.inner_steps):
            self.inner_opt.zero_grad()
            # step_loss = 0
            for x, y in task_support:
                y_pred = self.learner(x)
                loss = self.inner_loss(y_pred, y)
                loss.backward()
            # step_loss.backward()
            self.inner_opt.step()

    def fit(
        self, dataset, iterations: int, save_path: str, epoch: int, epochs_per_avg=1000
    ):
        self.learner.train()
        try:
            os.makedirs(save_path)
        except Exception:
            pass
        global_avg_inner_loss, global_avg_meta_loss, global_avg_accuracy, best_ckpt = (
            0,
            0,
            0,
            float("inf"),
        )
        for i in range(epoch, iterations):
            inner_loss, meta_loss, accuracy = self.train_on_batch(next(dataset))
            global_avg_inner_loss += inner_loss
            global_avg_meta_loss += meta_loss
            global_avg_accuracy += accuracy
            if i % epochs_per_avg == 0:
                if i != 0:
                    global_avg_inner_loss /= epochs_per_avg
                    global_avg_meta_loss /= epochs_per_avg
                    global_avg_accuracy /= epochs_per_avg
                print(
                    f"[{i}] Avg Inner Loss={global_avg_inner_loss} - Avg Outer Loss={global_avg_meta_loss} - Avg Outer Accuracy={accuracy:.2f} (over {epochs_per_avg} epochs) - Last Outer loss={meta_loss}"
                )
                if global_avg_meta_loss < best_ckpt:
                    torch.save(
                        {
                            "epoch": i,
                            "model_state_dict": self.learner.state_dict(),
                            "inner_opt_state_dict": self.inner_opt.state_dict(),
                            "meta_opt_state_dict": self.meta_opt.state_dict(),
                            "inner_loss": self.inner_loss,
                            "meta_loss": self.meta_loss,
                        },
                        os.path.join(
                            save_path,
                            f"epoch_{i}_loss-{global_avg_meta_loss:.6f}_accuracy-{global_avg_accuracy:.2f}.tar",
                        ),
                    )
                    best_ckpt = global_avg_meta_loss
                global_avg_inner_loss = 0
                global_avg_meta_loss = 0
                global_avg_accuracy = 0

    # def eval_with_higher(self, dataset):
    # total_loss, batch_size, avg_batch_loss = 0, 32, 0
    # batch_count = len(dataset)//batch_size + 1
    # for i in tqdm(range(batch_count)):
    # start = i*batch_size
    # end = min(len(dataset), start + batch_size)
    # avg_batch_loss += self.eval_task_batch(dataset[start:end])
    #     print(f"Total average loss: {avg_batch_loss/batch_count}")

    def eval(self, dataset, compute_accuracy=False):
        def fit_and_test(task, state_dict, comp_acc=False):
            # Restore the model parameters
            self.learner.load_state_dict(state_dict)
            self.adapt(task[0])
            task_loss, task_accuracies = 0, []  # Average loss per point in the task
            with torch.no_grad():
                self.learner.eval()
                for x, y in task[1]:
                    y_pred = self.learner(x)
                    task_loss += self.inner_loss(y_pred, y)
                    if comp_acc:
                        _, indices = y_pred.max(dim=1)
                        mean_acc = (y == indices).sum() / y.size(0)
                        task_accuracies.append(mean_acc)  # Mean accuracy per batch
            # Average per item because the inner loss reduction is 'sum'
            return (
                task_loss.div_(len(task[1].dataset)),
                torch.tensor(task_accuracies).mean(),
            )

        total_loss, total_acc = [], []
        # Save the model parameters
        state_dict = deepcopy(self.learner.state_dict())
        t = tqdm(total=len(dataset))
        for i, batch in enumerate(dataset):
            if not batch:
                t.close()
                break
            batch_loss, batch_accuracy = [], []
            for task in batch:
                loss, acc = fit_and_test(task, state_dict, comp_acc=compute_accuracy)
                batch_loss.append(loss)
                batch_accuracy.append(acc)
            total_loss.append(torch.tensor(batch_loss).mean())
            total_acc.append(torch.tensor(batch_accuracy).mean())
            t.update(len(batch))
        total_loss = torch.tensor(total_loss).mean().item()
        total_acc = torch.tensor(total_acc).mean().item() if compute_accuracy else 0.0
        print(
            f"Total average loss: {total_loss} - Total average accuracy: {total_acc:.4f}"
        )

    def restore(self, checkpoint, resume_training=True):
        self.learner.load_state_dict(checkpoint["model_state_dict"])
        self.meta_opt.load_state_dict(checkpoint["meta_opt_state_dict"])
        self.meta_loss = checkpoint["meta_loss"]
        if resume_training:
            self.inner_opt.load_state_dict(checkpoint["inner_opt_state_dict"])
            self.inner_loss = checkpoint["inner_loss"]
def MAML_train(
    dataset,
    learner,
    save_path: str,
    steps: int,
    meta_batch_size: int,
    iterations: int,
    checkpoint=None,
    loss_fn=None,
):
    print("[*] Training...")
    model = MAML(learner, steps=steps, loss_function=loss_fn)
    model.to(device)
    epoch = 0
    if checkpoint:
        model.restore(checkpoint)
        epoch = checkpoint["epoch"]
    model.fit(dataset, iterations, save_path, epoch, 100)
    print("[*] Done!")
    return model


def MAML_test(dataset, learner, checkpoint, steps, loss_fn):
    print("[*] Testing...")
    model = MAML(learner, steps=steps, loss_function=loss_fn)
    model.to(device)
    if checkpoint:
        model.restore(checkpoint, resume_training=False)
    else:
        print("[!] You are running inference on a randomly initialized model!")
    model.eval(dataset, compute_accuracy=(type(dataset) is OmniglotDataset))
    print("[*] Done!")


def parse_args():
    parser = argparse.ArgumentParser(description="Model-Agnostic Meta-Learning")
    parser.add_argument(
        "--checkpoint_path",
        type=str,
        help="""path to checkpoint
            saving directory""",
        default="ckpt",
    )
    parser.add_argument(
        "--load",
        type=str,
        help="""path to model
            checkpoint""",
    )
    parser.add_argument(
        "--eval",
        action="store_true",
        help="""Evaluation
    moed""",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=25,
        help="""Number of
    samples per task. The resulting number of test samples will be this value
    minus <K>.""",
    )
    parser.add_argument(
        "-k",
        type=int,
        default=10,
        help="""Number of shots
    for meta-training""",
    )
    parser.add_argument(
        "-q",
        type=int,
        default=15,
        help="""Number of
    meta-testing samples""",
    )
    parser.add_argument(
        "-n",
        type=int,
        default=5,
        help="""Number of classes for n-way
    classification""",
    )
    parser.add_argument(
        "-s",
        type=int,
        default=1,
        help="""Number of inner loop
    optimization steps during meta-training""",
    )
    parser.add_argument("--dataset", choices=["omniglot", "sinusoid", "harmonic"])
    parser.add_argument(
        "--meta-batch-size",
        type=int,
        default=25,
        help="""Number
    of tasks per meta-update""",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=80000,
        help="""Number
    of outer-loop iterations""",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    # np.random.seed(5)
    learner = ConvNetClassifier(device, 1, 20)
    checkpoint = None
    if args.load:
        checkpoint = torch.load(args.load)
    learner.to(device)
    if args.eval:
        test_dataset = OmniglotDataset(1, 28, args.k, args.q, args.n, evaluation=True)
        MAML_test(
            test_dataset,
            learner,
            checkpoint,
            args.s,
            torch.nn.MSELoss(reduction="sum")
            if args.dataset == "sinusoid"
            else torch.nn.CrossEntropyLoss(reduction="sum"),
        )
    else:
        train_dataset = OmniglotDataset(args.meta_batch_size, 28, args.k, args.q, args.n, evaluation=False)
        MAML_train(
            train_dataset,
            learner,
            args.checkpoint_path,
            args.s,
            args.meta_batch_size,
            args.iterations,
            checkpoint,
            torch.nn.CrossEntropyLoss(reduction="sum")
        )


if __name__ == "__main__":
    main()
