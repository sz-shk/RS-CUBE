<?php
session_start();
include("connect.php");

?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Homepage</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="homepage.css">
</head>
<body>
<header>
        <div class="logo">MyWebsite</div>
        <nav>
            <a href="#">Home</a>
            <a href="#">Profile</a>
            <a href="#">Settings</a>
            <a href="logout.php"onclick="logout()">Logout </a>

        </nav>
        <div class="welcome-message">
            Welcome, 
            <?php 
       if(isset($_SESSION['email'])){
        $email=$_SESSION['email'];
        $query=mysqli_query($conn, "SELECT users.* FROM `users` WHERE users.email='$email'");
        while($row=mysqli_fetch_array($query)){
            echo $row['firstName'].' '.$row['lastName'];
        }
       }
       ?><span id="username"></span>!
        </div>
    </header>

    <main>
        <section class="dashboard">
            <div class="card">
                <h2>Recent Activity</h2>
                <p>You last logged in on January 24, 2025.</p>
            </div>
            <div class="card">
                <h2>Notifications</h2>
                <p>You have 3 unread messages.</p>
            </div>
            <div class="card">
                <h2>Quick Links</h2>
                <ul>
                    <li><a href="#">Account Details</a></li>
                    <li><a href="#">Settings</a></li>
                    <li><a href="#">Support</a></li>
                </ul>
            </div>
            <div class="card">
                <h2>Start Dashboard</h2>
                <button onclick="startDashboard()">Go to Dashboard</button>
            </div>
        </section>
    </main>

    <footer>
        <p>© 2025 MyWebsite | <a href="#">Terms of Service</a> | <a href="#">Privacy Policy</a></p>
    </footer>

    <script src="location.js"></script>
</body>
</html>