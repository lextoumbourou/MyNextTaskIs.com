/*
 * Return a date string in format hh:mm:ss
 */
function convert_to_date_string(seconds) {
    hours = Math.floor(seconds / (60 * 60));
    minutes = Math.floor((seconds - (hours * 60 * 60)) / 60);
    seconds = seconds - (minutes * 60) - (hours * (60*60));

    date_string = ('0' + hours).slice(-2) + ':';
    date_string = date_string + ('0' + minutes).slice(-2) + ':';
    date_string = date_string + ('0' + seconds).slice(-2);

    return date_string
}

/*
 * Convert a date string to total seconds or false if malformed
 */
function convert_from_date_string(date_string) {
    var date_string_pattern = new RegExp("[0-9][0-9]:[0-5][0-9]:[0-5][0-9]");
    if (!date_string_pattern.test(date_string)) {
        return false;
    }
    var date_split = date_string.split(":");
    var hours = parseInt(date_split[0]);
    var minutes = parseInt(date_split[1]);
    var seconds = parseInt(date_split[2]);

    return (hours * 60 * 60) + (minutes * 60) + seconds;
}

/*
 * Convert a number of seconds to an english language 
 * date like 4 hours, 3 minutes and 1 second
 */
function convert_to_english(total_seconds) {
    hours = Math.floor(total_seconds / (60 * 60));
    minutes = Math.floor((total_seconds - (hours * 60 * 60)) / 60);
    seconds = total_seconds - (minutes * 60) - (hours * (60*60));

    output = "";
    if (hours) {
        output = output + hours;
        hour_string = hours === 1 ? " hour" : " hours";
        output = output + hour_string;
    };
    if (minutes) {
        if (hours && !seconds) {
            output = output + " and ";
        }
        else if (hours) {
            output = output + ", ";
        };
        minute_string = minutes === 1 ? " minute" : " minutes";
        output = output + minutes + minute_string
        if (seconds) {
            output = output + " and ";
        };
    }
    if (seconds || (!hours && !minutes && !seconds))
    {
        if (!minutes && hours) {
            output = output + " and "
        };
        second_string = seconds === 1 ? " second" : " seconds";
        output = output + seconds + second_string;
    };

    return output;
}

function Task(data) {
    var self = this;
    self.pk = ko.observable(data.pk);
    self.task = ko.observable(data.fields.task);
    self.is_complete = ko.observable(data.fields.is_complete);
    self.timer = ko.observable('00:00:00');
    self.timer_is_running = ko.observable(false);
    self.time_taken = ko.observable(data.fields.time_taken ? data.fields.time_taken : 0);
    self.editing_time = ko.observable(false);
    self.editing_title = ko.observable(false);
    self.start_time = ko.observable(
        data.fields.start_time ? data.fields.start_time : null);
    self.end_time = ko.observable(
        data.fields.end_time ? data.fields.end_time : null);

    self.update_time_taken = function(date_string) {
        console.log(date_string);
    };

    self.complete_task = function() {
        if (!self.start_time()) {
            self.start_time(new Date().valueOf());
        };
        self.end_time(new Date().valueOf());
        self.is_complete(true);
    };

    self.start_timer = function() {
        if (!self.start_time()) {
            self.start_time(new Date().valueOf());
        };
        self.interval_id = setInterval(self.update_timer, 1000);
        self.timer_is_running(true);
    };

    self.pause_timer = function() {
        clearInterval(self.interval_id);
        self.timer_is_running(false);
    };

    self.update_timer = function() {
        self.time_taken(self.time_taken() + 1);
        date_string = convert_to_date_string(self.time_taken());
        self.timer(date_string);
    };

    self.edit_time = function() {
        self.editing_time(true);
    };

    self.edit_title = function() {
        self.editing_title(true);
    };

    self.formatted_date = ko.computed({
        read: function() {
            if (!self.editing_time()) {
                return convert_to_english(self.time_taken());
            }
            else {
                return convert_to_date_string(self.time_taken());
            }
        },
        write: function(value) {
            total_time = convert_from_date_string(value);
            if (total_time !== false) {
                self.time_taken(total_time);
            }
        }
    });

    self.time_as_editable = function() {
        return convert_to_date_string(self.time_taken());
    }
}

function TaskListViewModel() {
    var self = this;

    // Menu items
    self.sections = ['Now', 'Next', 'Complete']

    self.chosen_section_id = ko.observable();
    
    // Behaviours
    self.go_to_section = function(section) {
        location.hash = section;
    };

    self.empty_task = function() {
        return new Task({pk: 0, fields: { task:"", is_complete:false }});
    };


    self.in_progress_task = ko.observable(self.empty_task());
    self.completed_tasks = ko.observableArray([]);
    self.incomplete_tasks = ko.observableArray([self.empty_task()]);
    self.date = $("#page_date").val();
    self.all_data = {};


    var KBD_ENTER = 13;
    self.enter_event = function(data, event) {
        if (event.which == KBD_ENTER) {
            self.add_empty_task();
        };

        return true;
    };

    self.add_empty_task = function() {
        self.incomplete_tasks.push(self.empty_task());
    };

    $.getJSON('/api/task', function(allData) {
        if (!$.isEmptyObject(allData)) {
            if (!allData[0].fields.is_complete) {
                self.in_progress_task(new Task(allData[0]));
            }

            var mapped_tasks = $.map(allData, function(item) {
                if (item.fields.is_complete) {
                    return new Task(item)
                }
            });
            self.completed_tasks(mapped_tasks);
        }
    });

    self.delete_task = function(task) {
        if (task.pk()) {
            $.ajax("/api/task/"+task.pk(), {
                type: "delete",
                success: function() {
                    self.in_progress_task(self.empty_task());
                },
            });
        };
    };

    self.save = function(task) {
        url = '/api/task/'
        if (task.pk() != 0) {
            url = url + task.pk()
        }

        $.ajax(url, {
            data: ko.toJSON(task),
            type: "post", 
            dataType: "json",
            success: function(allData) {
                task.pk(allData[0].pk);
            },
        });
    };

    self.update_completed = function(task) {
        task.pause_timer();
        self.completed_tasks.push(task);
        self.in_progress_task(self.empty_task());
    };

     // Animation callbacks for the planets list
    self.show_task_element = function(elem) { 
        if (elem.nodeType === 1) $(elem).hide().fadeIn() 
    };

    self.hide_task_element = function(elem) { 
        if (elem.nodeType === 1) $(elem).fadeOut(function() { $(elem).remove(); }) 
    };

    Sammy(function() {
        this.get('/#Now', function() {
            self.incomplete_tasks(null);
            self.chosen_section_id('Now');
            var url = ('/api/get_active_task');
            $.getJSON(url, function(data) {
                if (data[0]) {
                    self.in_progress_task(new Task(data[0]));
                }
                else {
                    self.in_progress_task(self.empty_task());
                }
            });
        });
        this.get('/#Next', function() {
            self.chosen_section_id('Next');
            self.in_progress_task(null);
            var url = ('/api/task');
            $.getJSON(url, function(data) {
                if (data.length > 0)
                {
                    var mapped_tasks = $.map(data, function(item) {
                            return new Task(item)
                    });
                    self.incomplete_tasks(mapped_tasks);
                }
                else
                {
                    self.incomplete_tasks([self.empty_task()]);
                }
            });
        });
        this.get('/#Complete', function() {
            self.chosen_section_id('Complete');
            self.in_progress_task(null);
        });
    }).run();


};

var task_list_model = new TaskListViewModel()
ko.applyBindings(task_list_model);
