function convert_to_date_string(seconds) {
    hours = Math.floor(seconds / (60 * 60));
    minutes = Math.floor((seconds - (hours * 60 * 60)) / 60);
    seconds = seconds - (minutes * 60) - (hours * (60*60));

    date_string = ('0' + hours).slice(-2) + ':';
    date_string = date_string + ('0' + minutes).slice(-2) + ':';
    date_string = date_string + ('0' + seconds).slice(-2);

    return date_string
}

function Task(data) {
    var self = this;
    this.pk = ko.observable(data.pk);
    this.task = ko.observable(data.fields.task);
    this.is_complete = ko.observable(data.fields.is_complete);
    this.timer = ko.observable('00:00:00');
    this.timer_is_running = ko.observable(false);
    self.time_taken = ko.observable(data.fields.time_taken ? data.fields.time_taken : 0);

    this.complete_task = function() {
        self.is_complete(true);
    };

    this.start_timer = function() {
        self.interval_id = setInterval(self.update_timer, 1000);
        self.timer_is_running(true);
    }

    this.pause_timer = function() {
        clearInterval(self.interval_id);
        self.timer_is_running(false);
    }

    this.update_timer = function() {
        self.time_taken(self.time_taken() + 1);
        date_string = convert_to_date_string(self.time_taken());
        self.timer(date_string);
    };

    this.time_as_english = function() {
        hours = Math.floor(self.time_taken() / (60 * 60));
        minutes = Math.floor((self.time_taken() - (hours * 60 * 60)) / 60);
        seconds = self.time_taken() - (minutes * 60) - (hours * (60*60));

        output = "";
        if (hours) {
            output = output + hours;
            hour_string = hours === 1 ? " hour" : " hours";
            output = output + hour_string;
        };
        if (minutes) {
            if (output != "") {
                output = output + ", ";
            };
            minute_string = minutes === 1 ? " minute" : " minutes";
            output = output + minutes + minute_string + " and ";
        };
        second_string = seconds === 1 ? " second" : " seconds";
        output = output + seconds + second_string;

        return output;
    };
}

function TaskListViewModel() {
    var self = this;
    this.empty_task = function() {
        return new Task({pk: 0, fields: { task:"", is_complete:false }});
    };

    this.completed_tasks = ko.observableArray([]);
    this.incomplete_task = ko.observable(self.empty_task());
    this.date = $("#page_date").val();
    this.all_data = {};

    $.getJSON('/api/task', function(allData) {
        if (!$.isEmptyObject(allData)) {
            if (!allData[0].fields.is_complete) {
                self.incomplete_task(new Task(allData[0]));
            }

            var mapped_tasks = $.map(allData, function(item) {
                if (item.fields.is_complete) {
                    return new Task(item)
                }
            });
            self.completed_tasks(mapped_tasks);
        }
    });

    this.delete_task = function(task) {
        if (task.pk()) {
            $.ajax("/api/task/"+task.pk(), {
                type: "delete",
                success: function() {
                    self.incomplete_task(self.empty_task());
                },
            });
        };
    };

    this.save = function(task) {
        url = '/api/task/'
        if (task.pk() != 0) {
            url = url + task.pk()
        }

        $.ajax(url, {
            data: ko.toJSON(
                {'task': task.task(), 'is_complete': task.is_complete(), 
                 'time_taken': task.time_taken,}),
            type: "post", 
            dataType: "json",
            success: function(allData) {
                if (task.is_complete()) {
                    
                }
                task.pk(allData[0].pk);
            },
        });
    };

    this.update_completed = function(task) {
        task.pause_timer();
        self.completed_tasks.push(task);
        self.incomplete_task(self.empty_task());
    };

     // Animation callbacks for the planets list
    this.show_task_element = function(elem) { 
        if (elem.nodeType === 1) $(elem).hide().fadeIn() 
    }

    this.hide_task_element = function(elem) { 
        if (elem.nodeType === 1) $(elem).fadeOut(function() { $(elem).remove(); }) 
    }
};

var task_list_model = new TaskListViewModel()
ko.applyBindings(task_list_model);
