import React, { Component } from "react";
import axios from "axios";

import CustomNavbar from "../components/UI/Navbar/Navbar";
import "../App.css";

class Tasks extends Component {
  state = {
    todoList: [],
    activeItem: {
      id: null,
      name: "",
      done: false,
    },
    editing: false,
  };

  // Creating csrf token
  getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  componentWillMount() {
    this.fetchTasks();
  }

  // Fetching items from database
  fetchTasks = () => {
    console.log("Fetching...");
    const bucketID = this.props.match.params.bucketID;
    axios
      .get(`http://127.0.0.1:8000/api/bucket/${bucketID}/tasks`)
      .then((res) => {
        this.setState({ todoList: res.data });
      });
  };

  // On input change
  handleChange = (e) => {
    this.setState({
      activeItem: {
        ...this.state.activeItem,
        [e.target.id]: e.target.value,
      },
    });
  };

  // After submit button
  handleSubmit = (e) => {
    e.preventDefault();
    console.log("ITEM:", this.state.activeItem);
    const bucketID = this.props.match.params.bucketID;

    let form_data = new FormData();
    const csrftoken = this.getCookie("csrftoken");
    let url = `http://127.0.0.1:8000/api/bucket/${bucketID}/task-create/`;

    form_data.append("name", this.state.activeItem.name);

    // Updating an item
    if (this.state.editing) {
      url = `http://127.0.0.1:8000/api/bucket/${bucketID}/task-update/${this.state.activeItem.id}/`;
      this.setState({
        editing: false,
      });
    }

    // Creating an item
    axios
      .post(url, form_data, {
        headers: {
          "content-type": `multipart/form-data;`,
          "X-CSRFToken": csrftoken,
        },
      })
      .then((res) => {
        this.fetchTasks();
        this.setState({
          activeItem: {
            id: null,
            name: "",
          },
        });
      })
      .catch((err) => console.log("ERROR:", err));
  };

  startEdit = (task) => {
    this.setState({
      activeItem: task,
      editing: true,
    });
  };

  deleteItem = (task) => {
    var csrftoken = this.getCookie("csrftoken");
    const bucketID = this.props.match.params.bucketID;

    fetch(
      `http://127.0.0.1:8000/api/bucket/${bucketID}/task-delete/${task.id}/`,
      {
        method: "DELETE",
        headers: {
          "Content-type": "application/json",
          "X-CSRFToken": csrftoken,
        },
      }
    ).then((response) => {
      this.fetchTasks();
    });
  };

  strikeUnstrike = (task) => {
    task.done = !task.done;
    const csrftoken = this.getCookie("csrftoken");
    const bucketID = this.props.match.params.bucketID;
    const url = `http://127.0.0.1:8000/api/bucket/${bucketID}/task-update/${task.id}/`;
    const data = JSON.stringify({ done: task.done, name: task.name });

    axios
      .post(url, data, {
        headers: {
          "Content-type": "application/json",
          "X-CSRFToken": csrftoken,
        },
      })
      .then((res) => {
        this.fetchTasks();
      })
      .catch((err) => console.log("ERROR:", err));
  };

  render() {
    var tasks = this.state.todoList;
    var self = this;

    return (
      <>
        <CustomNavbar />
        <div className="container">
          <div id="item-container">
            <center>
              <h2>Add/Edit Task</h2>
            </center>
            <div id="form-wrapper">
              <form onSubmit={this.handleSubmit} id="form">
                <div className="flex-wrapper">
                  <div style={{ flex: 6 }}>
                    <input
                      onChange={this.handleChange}
                      className="form-control"
                      id="name"
                      value={this.state.activeItem.name}
                      type="text"
                      name="name"
                      placeholder="Add task.."
                      required
                    />
                  </div>

                  <div style={{ flex: 1 }}>
                    <input
                      id="submit"
                      className="btn btn-warning"
                      type="submit"
                      name="Add"
                    />
                  </div>
                </div>
              </form>
            </div>

            <div id="list-wrapper">
              <center>
                <h2>Tasks</h2>
              </center>
              {tasks.map(function (task, index) {
                return (
                  <div key={index} className="item-wrapper flex-wrapper">
                    <div
                      onClick={() => self.strikeUnstrike(task)}
                      style={{ flex: 7 }}
                    >
                      {task.done == false ? (
                        <span>{task.name}</span>
                      ) : (
                        <strike>{task.name}</strike>
                      )}
                    </div>

                    <div style={{ flex: 1 }}>
                      <button
                        onClick={() => self.startEdit(task)}
                        className="btn btn-sm btn-outline-info"
                      >
                        Edit
                      </button>
                    </div>

                    <div style={{ flex: 1 }}>
                      <button
                        onClick={() => self.deleteItem(task)}
                        className="btn btn-sm btn-outline-danger delete"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </>
    );
  }
}

export default Tasks;
