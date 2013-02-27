function Task(data) {
    var self = this;
    this.pk = ko.observable(data.pk);
    this.task = ko.observable(data.fields.task);
    this.is_complete = ko.observable(data.fields.is_complete);
    self.remove_task = function() {
        self.is_complete(false);
        self.task("");
    };
    self.complete_task = function() {
        self.is_complete(true);
    };
}

function TaskListViewModel() {
    var self = this;

    self.completed_tasks = ko.observableArray([]);
    self.incomplete_task = ko.observableArray([]);
    self.date = $("#page_date").val();

    $.getJSON("/get_tasks?&date="+self.date, function(allData) {
        self.assign_to_arrays(allData);
    });

    self.save = function() {
        console.log(ko.toJSON(self.incomplete_task()[0]));
        $.ajax("/update_task?date="+self.date, {
            data: ko.toJSON(self.incomplete_task()[0]),
            type: "post", 
            dataType: "json",
            success: function(allData) {
                self.assign_to_arrays(allData);
            },
        });
    };

    self.assign_to_arrays = function(allData) {
        // Due to the way the backend works, 
        // the first task will always be the incomplete
        if (!$.isEmptyObject(allData) && allData[0].is_complete) {
            task = [new Task({pk: 0, fields: { task:"", is_complete:false }})];
        }
        else {
            task = [new Task(allData[0])];
        }
        self.incomplete_task(task);

        if (!$.isEmptyObject(allData)) {
            var mapped_tasks = $.map(allData, function(item) {
                if (item.fields.is_complete) {
                    return new Task(item)
                }
            });
            self.completed_tasks(mapped_tasks);
        }
    };

    self.clear_task = function() {
        self.incomplete_task(
            [new Task({pk: 0, fields: { task:"", is_complete:false }})]);
    };
};

var task_list_model = new TaskListViewModel()
ko.applyBindings(task_list_model);
