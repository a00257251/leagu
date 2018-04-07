<?php
$conn = mysqli_connect("localhost", "root", "","students");

if (!$conn) {
die("Connection failed: " . mysqli_connect_error());
}

if(isset($_POST['submit'])) {
$user = $_POST['user'];
$pass = $_POST['pass'];

$query= "SELECT * FROM `login` WHERE username= '$user' AND password ='$pass'";

$result = mysqli_query($conn,$query);

if (!$result) {
printf("Error: %s\n", mysqli_error($conn));
exit();
}

$row = mysqli_num_rows($result);
if($row >0){header("location: singin.php");}
else{
?>
<script>
alert("Invalid Username or Password !");
</script>
<?php  
}
mysqli_close($conn);
}

?>


<!DOCTYPE html>
<html>
<head>
<title>Graduates Registration</title>
<link rel="stylesheet" href="main.css">
<!--<script src="index.js"></script>-->
 
</head>
<body>    
<ul id="m">
<img src="aitt.png" class="nav" id="ait">
<li class="nav"><a href="home.html">Home</a></li>
<li class="nav"><a href="https://www.ait.ie">AIT Home page</a></li>
<li class="nav"><a href="indexx.html">Staff Login</a></li>
<li class="nav"><a href="http://timetable.ait.ie/students.htm">Student Timetable</a></li>
<li class="dropdown">
    <a href="https://www.ait.ie/life-at-ait/registry/graduation" class="dropbtn">Graduation</a>
<div class="dropdown-content">
<a href="https://www.ait.ie/life-at-ait/registry/graduation">Graduation Timetable</a>
<a href="https://www.lafayette.ie ">Graduation Photography</a>
<a href="https://www.phelanconan.com/">Academic Dress</a>
<a href="https://www.ait.ie/life-at-ait/registry/graduation">Graduation Ball</a>
<a href="https://www.ait.ie/life-at-ait/registry/graduation">Assembly Point</a>
<li class="nav"><a href="location.html">Graduation Location</a></li>
<li class="nav"><a href="contact.html">Contact us</a></li>
</ul>

<body background="kkk2.jpg"/>
<div class="container">
<div class="s">
<img src="login10.png" id="logo"/>
<form action="" method="post">
<h2>AIT Student Login</h2>
<ul>
<li>
<label for="user">Username :</label>
<input type="text" id="user" name="user" class="text" placeholder="Enter your student number" required>
</li>
<li>
<label for="pass">Password :</label>
<input type="password" id="pass" name="pass" class="text" placeholder="Enter your student password" required>
</li>
<li>
<label for="submit">&nbsp;</label>
<input type="submit" id="submit" name="submit" value="Login">
</li>
</ul>
</form>  
</div>  
</div>
</body>
<footer>
<div class="foot">
<p>Get social with us..
<a href="https://twitter.com/AthloneIT?lang=en"><img src="t.gif" class="foo"></a>
<a href="https://www.facebook.com/athloneit/"><img src="f.gif" class="foo"></a>
<a href="https://www.linkedin.com/school/860289/"><img src="i.gif" class="foo"></a></p>
</div>
</footer>

</html>

