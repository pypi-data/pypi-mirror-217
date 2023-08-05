# -*- coding: utf-8 -*-

##
# Tiny ai helper
# Copyright (с) Ildar Bikmamatov 2022 - 2023 <support@bayrell.org>
# License: MIT
##

import torch, time, json, math, gc, os
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
from .utils import TransformDataset, list_files, \
    get_default_device, batch_to, tensor_size, load_json, summary, fit


class Model:
    
    def __init__(self, module=None):
        self.device = 'cpu'
        self.transform_x = None
        self.transform_y = None
        self.module = module
        self.optimizer = None
        self.scheduler = None
        self.loss = None
        self.loss_reduction = 'mean'
        self.loss_precision = 9
        self.best_metrics = ["epoch"]
        self.acc_fn = None
        self.acc_reduction = 'sum'
        self.name = module.__class__.__name__
        self.prefix_name = ""
        self.epoch = 0
        self.history = {}
        self.min_lr = 1e-5
        self.max_best_models = 50
        self.model_path = ""
        self.repository_path = ""
        self.set_repository_path("model")
    
    
    def set_module(self, module):
        self.module = module
        return self
    
    def set_optimizer(self, optimizer):
        self.optimizer = optimizer
        return self
    
    def set_loss(self, loss):
        self.loss = loss
        return self
    
    def set_scheduler(self, scheduler):
        self.scheduler = scheduler
        return self
    
    def set_acc(self, acc):
        self.acc_fn = acc
        return self
    
    def set_name(self, name):
        self.name = name
        self.set_repository_path(self.repository_path)
        return self
    
    def set_prefix_name(self, prefix_name):
        self.prefix_name = prefix_name
        self.set_repository_path(self.repository_path)
        return self
    
    def set_path(self, model_path):
        self.model_path = model_path
        return self
    
    def set_repository_path(self, repository_path):
        self.repository_path = repository_path
        self.model_path = os.path.join(repository_path, self.get_full_name())
        return self
    
    def get_full_name(self):
        if self.prefix_name != "":
            return self.name + "_" + self.prefix_name
        return self.name
    
    
    def to(self, device):
        self.module = self.module.to(device)
        self.device = device
        return self
    
    def to_cuda(self):
        self.to( torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu') )
        return self
    
    def to_cpu(self):
        self.to( torch.device("cpu") )
        return self
    
    def train(self):
        self.module.train()
        return self
    
    def eval(self):
        self.module.eval()
        return self
    
    
    def load_state_dict(self, save_metrics, strict=False):
        
        if "epoch" in save_metrics:
            self.epoch = save_metrics["epoch"]
            
            # Load history
            if "history" in save_metrics:
                self.history = save_metrics["history"].copy()
            
            # Load module
            if "module" in save_metrics:
                state_dict = save_metrics["module"]
                self.module.load_state_dict(state_dict, strict=strict)
            
            # Load optimizer
            if "optimizer" in save_metrics:
                state_dict = save_metrics["optimizer"]
                self.optimizer.load_state_dict(state_dict)
            
            # Load scheduler
            if "scheduler" in save_metrics:
                state_dict = save_metrics["scheduler"]
                self.scheduler.load_state_dict(state_dict)
            
            # Load loss
            #if "loss" in save_metrics:
            #    state_dict = save_metrics["loss"]
            #    self.loss.load_state_dict(state_dict)
        
        else:
            self.module.load_state_dict(save_metrics, strict=strict)
        
        return self
    
    
    def load_model(self, file_path, full_path=False):
        
        """
        Load model from file
        """
        
        if not os.path.exists(file_path) and not full_path:
            file_path = os.path.join(self.model_path, file_path)
        
        save_metrics = torch.load(file_path)
        self.load_state_dict(save_metrics)
        
        return self
        
    
    def load_epoch(self, epoch):
        
        """
        Load epoch
        """
        
        file_name = self.get_full_name() + "-" + str(epoch) + ".data"
        file_path = os.path.join(self.model_path, file_name)
        
        if not os.path.exists(file_path):
            file_name = self.get_full_name() + "-" + str(epoch) + ".pth"
            file_path = os.path.join(self.model_path, file_name)
        
        self.load_model(file_path, full_path=True)
        
        return self
        
        
    def load_last(self):
        
        """
        Load last model
        """
        
        file_name = self.get_full_name() + ".data"
        file_path = os.path.join(self.model_path, file_name)
        
        if not os.path.exists(file_path):
            file_name = self.get_full_name() + ".pth"
            file_path = os.path.join(self.model_path, file_name)
        
        if os.path.exists(file_path):
            self.load_model(file_path, full_path=True)
            return self
        
        file_name = os.path.join(self.model_path, "history.json")
        if os.path.exists(file_name):
        
            obj = load_json(file_name)
            
            if obj is not None:
                epoch = obj["epoch"]
                self.load_epoch(epoch)
        
        return self
        
    
    def load_best(self):
        
        """
        Load best model
        """
        
        file_path = os.path.join(self.model_path, "history.json")
        
        if not os.path.exists(file_path):
            return self
        
        obj = load_json(file_path)
        
        if obj is not None:
            best_epoch = obj["best_epoch"]
            self.load_epoch(best_epoch)
        
        return self
    
    
    def save_weights_epoch(self, file_path=None):
        
        """
        Save weights
        """
        
        if file_path is None:
            file_name = self.get_full_name() + "-" + str(self.epoch) + ".pth"
            file_path = os.path.join(self.model_path, file_name)
        
        torch.save(self.module.state_dict(), file_path)
        
        return self
    
    
    def save_weights(self, file_path=None):
        
        """
        Save weights
        """
        
        if file_path is None:
            file_name = self.get_full_name() + ".pth"
            file_path = os.path.join(self.model_path, file_name)
        
        torch.save(self.module.state_dict(), file_path)
        
        return self
    
    
    def save_train_epoch(self):
        
        """
        Save train epoch
        """
        
        file_name = self.get_full_name() + "-" + str(self.epoch) + ".data"
        file_path = os.path.join(self.model_path, file_name)
        self.save_model(file_path)
        
        return self
    
        
    def save_model(self, file_path=None):
        
        """
        Save train status
        """
        
        # Get metrics
        save_metrics = {}
        save_metrics["name"] = self.get_full_name()
        save_metrics["epoch"] = self.epoch
        save_metrics["history"] = self.history.copy()
        save_metrics["module"] = self.module.state_dict()
        
        if self.optimizer is not None:
            save_metrics["optimizer"] = self.optimizer.state_dict()
        
        if self.scheduler is not None:
            save_metrics["scheduler"] = self.scheduler.state_dict()
        
        #if self.loss is not None:
        #    save_metrics["loss"] = self.loss.state_dict()
        
        # Create folder
        if not os.path.isdir(self.model_path):
            os.makedirs(self.model_path)
        
        # Save model to file
        if file_path is None:
            model_file_name = self.get_full_name() + ".data"
            file_path = os.path.join(self.model_path, model_file_name)
        
        torch.save(save_metrics, file_path)
        
        return self
    
    
    def save_history(self):
        
        """
        Save history to json
        """
        
        best_epoch = self.get_the_best_epoch()
        file_name = os.path.join(self.model_path, "history.json")
        obj = {
            "epoch": self.epoch,
            "best_epoch": best_epoch,
            "history": self.history.copy(),
        }
        json_str = json.dumps(obj, indent=2)
        file = open(file_name, "w")
        file.write(json_str)
        file.close()
        
        return self
    
    
    def do_training(self, max_epochs):
        
        """
        Returns True if model is need to train
        """
        
        if self.epoch >= max_epochs:
            return False
        
        for item in self.optimizer.param_groups:
            if item["lr"] >= self.min_lr:
                return True
        
        return False
    
    
    def set_new_lr(self, lr):
        
        for index, param_group in enumerate(self.optimizer.param_groups):
            param_group['lr'] = lr[index]
        
        return self
    
    
    def __call__(self, x):
        return self.module(x)
    
    
    def predict(self, x):
        
        """
        Predict
        """
        
        batch_transform = getattr(self.module, "batch_transform", None)
        
        with torch.no_grad():
            
            x = x.to(self.device)
            if batch_transform:
                x, _ = batch_transform(x)
            
            self.module.eval()
            y = self.module(x)
        
        return y
    
    
    def predict_dataset(self, dataset, predict, batch_size=64, obj=None):
        
        """
        Predict dataset
        """
        
        device = self.device
        loader = DataLoader(
            dataset,
            batch_size=batch_size,
            drop_last=False,
            shuffle=False
        )
        
        batch_transform = getattr(self.module, "batch_transform", None)
        
        with torch.no_grad():
        
            self.module.eval()
            
            pos = 0
            next_pos = 0
            dataset_count = len(dataset)
            time_start = time.time()
            
            for batch in loader:
                
                if batch_transform:
                    batch = batch_transform(batch)
                
                x_batch = batch["x"].to(device)
                y_batch = batch["y"].to(device)
                
                y_predict = self.module(x_batch)
                predict(batch, y_predict, obj)
                
                # Show progress
                pos = pos + len(x_batch)
                if pos > next_pos:
                    next_pos = pos + 16
                    t = str(round(time.time() - time_start))
                    print ("\r" + str(math.floor(pos / dataset_count * 100)) + "% " + t + "s", end='')
                
                del x_batch, y_batch, y_predict, batch
                
                # Clear cache
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                gc.collect()
            
            print ("\nOk")
    
    
    def get_metrics(self, metric_name, convert=False):
        
        """
        Returns metrics by name
        """
        
        def convert_value(value, metric_name):
            if (
                metric_name == "train_acc" or
                metric_name == "train_acc_value" or
                metric_name == "val_acc" or
                metric_name == "val_acc_value" or
                metric_name == "epoch"
            ):
                return -value
            return value
        
        res = []
        epochs = list(self.history.keys())
        for index in epochs:
            
            epoch = self.history[index]
            res2 = [ index ]
            
            if isinstance(metric_name, list):
                for name in metric_name:
                    value = epoch[name] if name in epoch else 0
                    if convert:
                        value = convert_value(value, name)
                    res2.append( value )
            
            else:
                value = epoch[metric_name] if metric_name in epoch else 0
                if convert:
                    value = convert_value(value, metric_name)
                res2.append( value )
            
            res.append(res2)
            
        return res
    
    
    def get_metric(self, metric_name, convert=False):
        
        """
        Returns metrics by name
        """
        
        res = []
        epochs = list(self.history.keys())
        for index in epochs:
            
            epoch = self.history[index]
                        
            value = epoch[metric_name] if metric_name in epoch else 0
            if convert:
                value = convert_value(value, metric_name)
            res.append( value )
            
        return res
    
    
    def get_the_best_epoch(self, best_metrics=None):
        
        """
        Returns the best epoch
        """
        
        epoch_indexes = self.get_the_best_epochs_indexes(1, best_metrics)
        best_epoch = epoch_indexes[0] if len(epoch_indexes) > 0 else 0
        return best_epoch
    
    
    def get_the_best_epochs_indexes(self, epoch_count=5, best_metrics=None):
        
        """
        Returns best epoch indexes
        """
        
        if best_metrics is None:
            best_metrics = self.best_metrics
        
        metrics = self.get_metrics(best_metrics, convert=True)
        metrics.sort(key=lambda x: x[1:])
        
        res = []
        res_count = 0
        metrics_len = len(metrics)
        loss_val_last = 100
        for index in range(metrics_len):
            
            res.append( metrics[index] )
            
            if loss_val_last != metrics[index][1]:
                res_count = res_count + 1
            
            loss_val_last = metrics[index][1]
            
            if res_count > epoch_count:
                break
        
        res = [ res[index][0] for index in range(len(res)) ]
        
        return res
    
    
    def get_best_epoch(self, best_metrics=None):
        
        """
        Returns the best epoch
        """
        
        return self.get_the_best_epoch(best_metrics)
    
    
    def get_best_epochs(self, epoch_count=5, best_metrics=None):
        
        """
        Returns best epoch indexes
        """
        
        return self.get_the_best_epochs_indexes(epoch_count, best_metrics)
    
    
    def save_the_best_models(self):
        
        """
        Save the best models
        """
        
        def detect_type(file_name):
            
            import re
            
            file_type = ""
            epoch_index = 0
            model_name = self.get_full_name()
            
            result = re.match(r'^'+model_name+'-(?P<id>[0-9]+)\.data$', file_name)
            if result:
                return "model", int(result.group("id"))
            
            result = re.match(r'^'+model_name+'-(?P<id>[0-9]+)\.pth$', file_name)
            if result:
                return "model", int(result.group("id"))
            
            return file_type, epoch_index
        
        
        epoch_count = self.max_best_models
        
        if self.epoch > 0 and epoch_count > 0 and os.path.isdir(self.model_path):
            
            epoch_indexes = self.get_the_best_epochs_indexes(epoch_count)
            epoch_indexes.append( self.epoch )
            
            files = list_files( self.model_path )
            
            for file_name in files:
                
                file_type, epoch_index = detect_type(file_name)
                if file_type in ["model"] and \
                    epoch_index > 0 and \
                    not (epoch_index in epoch_indexes):
                    
                    file_path = os.path.join( self.model_path, file_name )
                    os.unlink(file_path)
    
    
    def summary(self, x):
        
        """
        Show model summary
        """
        
        summary(self.module, x,
            device=self.device,
            model_name=self.get_full_name()
        )
    
        
    def draw_history_ax(self, ax, metrics=[], label=None, legend=True, convert=None, start=0):
        
        """
        Draw history to axes
        """
        
        metrics_values = self.get_metrics(metrics)
        metrics_values = metrics_values[start:]
        for index, name in enumerate(metrics):
            values = [ item[index + 1] for item in metrics_values ]
            if convert:
                values = list(map(convert, values))
            if len(values) > 0 and values[0] is not None:
                ax.plot( values, label=name)
        
        if label:
            ax.set_xlabel( label )
        
        if legend:
            ax.legend()
    
    
    def draw_history(self, show_acc=False, show_loss=True, start=0):
        
        """
        Draw history
        """
        
        import matplotlib.pyplot as plt
        
        pos = 0
        fig, ax = plt.subplots(1, show_acc + show_loss, figsize=(10, 4))
        if show_acc:
            self.draw_history_ax(
                ax[pos] if isinstance(ax, np.ndarray) else ax,
                ["train_acc", "val_acc"],
                label="Accuracy",
                convert=lambda x: x * 100 if x is not None else None,
                start=start
            )
            pos += 1
        if show_loss:
            self.draw_history_ax(
                ax[pos] if isinstance(ax, np.ndarray) else ax,
                ["train_loss", "val_loss"],
                label="Loss",
                start=start
            )
        plt.show()
    
    
    def print_history(self):
        
        h = list(self.history.keys())
        h.sort()
        
        for epoch in h:
            s = self.get_epoch_string(epoch)
            print(s)
    
    
    def get_epoch_train_status(self):
        
        status = {
            "epoch": self.epoch,
            "time_start": 0,
            "time_end": 0,
            "train_acc": None,
            "train_acc_items": [],
            "train_acc_sum": 0,
            "train_count": 0,
            "train_loss": None,
            "train_loss_items": [],
            "train_batch_iter": 0,
            "val_acc": None,
            "val_acc_items": [],
            "val_acc_sum": 0,
            "val_count": 0,
            "val_loss": None,
            "val_loss_items": [],
            "val_batch_iter": 0,
            "total_count": 0,
            "pos": 0,
            "t": 0,
        }
        
        if self.acc_fn is None:
            status["train_acc_sum"] = None
            status["val_acc_sum"] = None
        
        return status
    
    def add_epoch(self, **h):
    
        lr = []
        for param_group in self.optimizer.param_groups:
            lr.append( round(param_group['lr'], 7) )
        
        h["train_loss"] = None
        h["train_acc"] = None
        h["val_loss"] = None
        h["val_acc"] = None
        h["rel"] = None
        h["lr"] = lr
        
        train_count = h["train_count"]
        val_count = h["val_count"]
        
        if self.loss_reduction == "mean":
            
            if len(h["train_loss_items"]) > 0:
                h["train_loss"] = sum(h["train_loss_items"]) / len(h["train_loss_items"])
            
            if len(h["val_loss_items"]) > 0:
                h["val_loss"] = sum(h["val_loss_items"]) / len(h["val_loss_items"])
        
        elif self.loss_reduction == "sum":
            
            if len(h["train_loss_items"]) > 0 and train_count > 0:
                h["train_loss"] = sum(h["train_loss_items"]) / train_count
            
            if len(h["val_loss_items"]) > 0 and val_count > 0:
                h["val_loss"] = sum(h["val_loss_items"]) / val_count
        
        if self.acc_reduction == "mean":
            
            if len(h["train_acc_items"]) > 0:
                h["train_acc"] = sum(h["train_acc_items"]) / len(h["train_acc_items"])
            
            if len(h["val_acc_items"]) > 0:
                h["val_acc"] = sum(h["val_acc_items"]) / len(h["val_acc_items"])
        
        elif self.acc_reduction == "sum":
            
            if len(h["train_acc_items"]) > 0 and train_count > 0:
                h["train_acc"] = sum(h["train_acc_items"]) / train_count
            
            if len(h["val_acc_items"]) > 0 and val_count > 0:
                h["val_acc"] = sum(h["val_acc_items"]) / val_count
        
        if not(h["train_acc"] is None) and not(h["val_acc"] is None):
            h["rel"] = (h["train_acc"] / h["val_acc"]) if h["val_acc"] > 0 else 0
        
        epoch = h["epoch"]
        self.history[epoch] = h.copy()
    
    
    def get_epoch_string(self, epoch):
        
        res = self.history[epoch]
        
        # Get epoch status
        t = res["t"] if "t" in res else 0
        train_acc = res["train_acc"] if "train_acc" in res else 0
        train_loss = res["train_loss"] if "train_loss" in res else 0
        train_count = res["train_count"] if "train_count" in res else 0
        val_acc = res["val_acc"] if "val_acc" in res else 0
        val_loss = res["val_loss"] if "val_loss" in res else 0
        val_count = res["val_count"] if "val_count" in res else 0
        res_lr = res["lr"] if "lr" in res else []
        res_lr_str = str(res_lr)
        
        msg = []
        msg.append(f'\rEpoch: {epoch}')
        
        if not(train_acc is None):
            train_acc = round(train_acc * 10000) / 100
            msg.append(f'train_acc: {train_acc}%')
        
        if not(val_acc is None):
            val_acc = round(val_acc * 10000) / 100
            msg.append(f'val_acc: {val_acc}%')
        
        if "rel" in res and not(res["rel"] is None):
            acc_rel = round(res["rel"] * 1000) / 1000
            msg.append(f'rel: {acc_rel}')
        
        if not(train_loss is None):
            f = "{:."+str(self.loss_precision)+"f}"
            train_loss = f.format(train_loss)
            msg.append(f'train_loss: {train_loss}')
        
        if not(val_loss is None):
            f = "{:."+str(self.loss_precision)+"f}"
            val_loss = f.format(val_loss)
            msg.append(f'val_loss: {val_loss}')
        
        #msg.append(f'lr: {res_lr_str}')
        msg.append(f't: {t}s')
        
        return ", ".join(msg)
    
    
    def get_progress_string(self, kind, params, status):
        
        epoch = status["epoch"]
        train_count = status["train_count"]
        train_acc_items = status["train_acc_items"]
        train_loss_items = status["train_loss_items"]
        val_count = status["val_count"]
        val_acc_items = status["val_acc_items"]
        val_loss_items = status["val_loss_items"]
        
        iter_value = 0
        if status["total_count"] > 0:
            iter_value = status["pos"] / status["total_count"]
        iter_value = round(iter_value * 100)
        
        if kind == "train":
            
            train_acc_val = 0
            if len(train_acc_items) > 0:
                train_acc_sum = sum(train_acc_items)
                if self.acc_reduction == "sum":
                    if train_count > 0:
                        train_acc_val = round(train_acc_sum / train_count * 10000) / 100
                else:
                    train_acc_val = round(train_acc_sum / len(train_acc_items) * 10000) / 100
            
            if train_acc_val > 0:
                return f"Epoch: {epoch}, {iter_value}%, acc: {train_acc_val}%"
            else:
                return f"Epoch: {epoch}, {iter_value}%"
        
        if kind == "val":
            
            val_acc_val = 0
            if len(val_acc_items) > 0:
                val_acc_sum = sum(val_acc_items)
                if self.acc_reduction == "sum":
                    if val_count > 0:
                        val_acc_val = round(val_acc_sum / val_count * 10000) / 100
                else:
                    val_acc_val = round(val_acc_sum / len(val_acc_items) * 10000) / 100
            
            if val_acc_val > 0:
                return f"Epoch: {epoch}, {iter_value}%, acc: {val_acc_val}%"
            else:
                return f"Epoch: {epoch}, {iter_value}%"
    
    
    def get_train_loss(self, epoch=None):
        if epoch is None:
            epoch = self.epoch
        value = self.history[epoch]["train_loss"]
        if value is None:
            value = 0
        return value
    
    
    def get_val_loss(self, epoch=None):
        if epoch is None:
            epoch = self.epoch
        value = self.history[epoch]["train_loss"]
        if value is None:
            value = 0
        return value
    
    
    def get_train_acc(self, epoch=None):
        if epoch is None:
            epoch = self.epoch
        value = self.history[epoch]["train_acc"]
        if value is None:
            value = 0
        return value
    
    
    def get_val_acc(self, epoch=None):
        if epoch is None:
            epoch = self.epoch
        value = self.history[epoch]["train_acc"]
        if value is None:
            value = 0
        return value
    
    
    def get_epoch_metric(self, metric_name, epoch=None):
        if epoch is None:
            epoch = self.epoch
        value = self.history[epoch][metric_name]
        if value is None:
            value = 0
        return value
    
    
    def upload_to_google_drive(self, epoch, repository_path):
        
        import shutil
    
        if not os.path.exists('/content/drive'):
            from google.colab import drive
            drive.mount('/content/drive')
        
        dest_path = os.path.join(repository_path, self.get_full_name())
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        
        def upload(file_name):
            src_file_path = os.path.join(self.model_path, file_name)
            if os.path.exists(src_file_path):
                dest_file_path = os.path.join(dest_path, file_name)
                shutil.copy(src_file_path, dest_file_path)

        upload(self.get_full_name() + "-" + str(epoch) + ".data")
        upload(self.get_full_name() + "-" + str(epoch) + ".pth")
    
    
    def download_from_google_drive(self, epoch, repository_path):
        
        import shutil
        
        if not os.path.exists('/content/drive'):
            from google.colab import drive
            drive.mount('/content/drive')
        
        src_path = os.path.join(repository_path, self.get_full_name())
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        
        def download(file_name):
            src_file_path = os.path.join(src_path, file_name)
            if os.path.exists(src_file_path):
                dest_file_path = os.path.join(self.model_path, file_name)
                shutil.copy(src_file_path, dest_file_path)

        download(self.get_full_name() + "-" + str(epoch) + ".data")
        download(self.get_full_name() + "-" + str(epoch) + ".pth")
    
    
    def upload_history_to_google_drive(self, repository_path):
    
        import shutil
        
        if not os.path.exists('/content/drive'):
            from google.colab import drive
            drive.mount('/content/drive')
        
        if not os.path.exists(repository_path):
            os.makedirs(repository_path)
        
        dest_path = os.path.join(repository_path, self.get_full_name())
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        
        src_file_path = os.path.join(self.model_path, "history.json")
        dest_file_path = os.path.join(dest_path, "history.json")
        shutil.copy(src_file_path, dest_file_path)
    
    
    def download_history_from_google_drive(self, repository_path):
    
        import shutil
        
        if not os.path.exists('/content/drive'):
            from google.colab import drive
            drive.mount('/content/drive')
        
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        
        src_path = os.path.join(repository_path, self.get_full_name())
        src_file_path = os.path.join(src_path, "history.json")
        dest_file_path = os.path.join(self.model_path, "history.json")
        shutil.copy(src_file_path, dest_file_path)