function Task(data) {
    var self = this;
    self.pk = ko.observable(data.pk || '');
    self.task = ko.observable(data.task || '');
};

function NextTaskListViewModel() {
    var self = this;
    self.tasks = ko.observableArray([Task({})]);

    var KBD_ENTER = 13;
    self.enter_event = function(data, event) {
        if (event.which == KBD_ENTER) {
            self.add_empty_task();
        };

        return true;
    };

    self.add_empty_task = function() {
        self.tasks.push(Task({}));
    };
};

var task_list_model = new NextTaskListViewModel();
ko.applyBindings(task_list_model);

