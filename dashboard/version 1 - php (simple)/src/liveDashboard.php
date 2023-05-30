<!DOCTYPE html>

<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Production Live Dashboard</title>
    <link href="/dist/output.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/bootstrap-icons.css">
    <script src="/node_modules/tw-elements/dist/js/index.min.js"></script>
    
    <!-- This tailwind link is for php !important -->
    <script src="https://cdn.tailwindcss.com"></script>

</head>


<body class="bg-gray-100 font-sans leading-normal tracking-normal">

    <!-- DATABASE CONNECTION -->
    <?php
        $servername = "127.0.0.1";
        $username = "root";
        $password = "terrytyler23";
        $db = "industry";
        
        // Connect to database
        $conn = mysqli_connect($servername, $username, $password, $db);
        
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
    ?>

    <!-- Navbar -->
    <nav class="p-5 bg-white border-b border-gray-200">
        <!-- Flex container -->
        <div class="flex items-center justify-between">
            <!-- Logo -->
            <div class="pt-2">
            <img src="../img/WMU-primary.png" alt="logo" style="width: 12em; margin-top: -.7em;"/>
            </div>
            <!-- Menu Items -->
            <div class="hidden text-black space-x-6 md:flex">
            <a href="index.php" class="hover:text-darkGrayishBlue">Home</a>
            <a>|</a>
            <a href="#" class="hover:text-darkGrayishBlue">About Us</a>
            <a>|</a>
            <a href="#" class="hover:text-darkGrayishBlue">Recent</a>
            </div>
            <!-- Button -->
            <a
            href="/src/liveDashboard.html"
            class="p-3 px-6 pt-3 text-white bg-black rounded-full baseline hover:bg-gray-500"
            >
            Live Dashboard
            </a>
    
    
            <!-- Hamburger Icon -->
            <button
            id="menu-btn"
            class="block hamburger md:hidden focus:outline-none"
            >
            <span class="hamburger-top"></span>
            <span class="hamburger-middle"></span>
            <span class="hamburger-bottom"></span>
            </button>
        </div>

    </nav>

    

    <!-- Live Dashboard -->
    <section class="">

        <!-- Header -->
        <div>
            <h1 class="pt-12 text-center font-bold text-7xl">Live Dashboard</h1>
            <p class="pb-1 text-center text-md">View real-time updates and statistics.</p>
        <div>

        <!-- Session Key -->
        <form class="hidden">
            <div class="container mx-auto mt-32 text-center max-w-sm">
                <label for="key" class="font-bold text-xl mt-24">Session Key:</label>
                <input type="key" id="key" class="text-center bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="3490235" required>
                <button href="/src/liveDashboard.html" class="mt-3 p-3 px-6 pt-3 text-white bg-black rounded-full baseline hover:bg-gray-500 ">
                    Start Dashboard
                </button>
            </div>
        </form>

       <!-- Dashboard Content (Key Success) -->
        <div class="block">
             <!-- Edit Displays -->
            <div class="flex space-x-2 justify-center">
                <div>
                    <button type="button" class="bg-black text-white rounded-full drop-shadow-2xl py-1 mt-1 px-4 hover:bg-gray-500">Edit</button>
                </div>
            </div>

            <!-- Live Dashboard Content -->
            <div class="container mx-auto">
                <div class="grid grid-cols-3 gap-4 p-4">

                    <!-- Box 1 (Connection Status) -->
                    <div class="col-span-3 bg-white shadow-xl rounded-3xl p-4 border-2 border-gray-300">
                        <h1 class="mb-3 mt-1 py-1 rounded-t-lg text-center font-bold text-2xl bg-gray-300"><span><i class="bi bi-wifi"></i></span> Connection Status</h1>
                        
                        <!-- All Connections -->
                        <div class="grid grid-rows-1 grid-flow-col">
                            <div class="text-center text-3xl">
                                Tablets: <br>
                                <i class="text-2xl bi bi-check-circle-fill"></i>
                                <i class="text-2xl bi bi-check-circle-fill"></i>
                                <i class="text-2xl bi bi-3-circle-fill text-red-600"></i>
                                <i class="text-2xl bi bi-check-circle-fill"></i>
                            </div>
                            
                            <div class="text-center text-3xl">
                                Scanners: <br>
                                <i class="text-2xl bi bi-check-circle-fill"></i>
                                <i class="text-2xl bi bi-check-circle-fill"></i>
                                <i class="text-2xl bi bi-check-circle-fill"></i>
                                <i class="text-2xl bi bi-check-circle-fill"></i>
                            </div>

                            <div class="text-center text-3xl">
                                Printer:<br>
                                <i class="text-2xl bi bi-check-circle-fill"></i>
                            </div>

                            <div class="text-center text-3xl">
                                Camera:<br>
                                <i class="text-2xl bi bi-check-circle-fill"></i>
                            </div>
                        </div>


                        
                    </div>

                    <!-- Box 2 -->
                    <div class="bg-white shadow-xl rounded-3xl p-4 border-2 border-gray-300">
                        <h1 class="mb-3 py-1 text-center font-bold text-2xl rounded-t-lg bg-gray-300"><span><i class="bi bi-check2-square"></i></span> Completed Assemblies</h1>
                        
                        <!-- number of row in completed_assemblies where date = today -->
                        <?php
                            // open connection
                            $conn = mysqli_connect($servername, $username, $password, $db);

                            // Select the count of rows from the table where the date component of the datetime field is equal to the current date
                            $sql = "SELECT COUNT(*) FROM completed_assemblies WHERE DATE(completed_at) = CURDATE()";

                            // Execute the query and store the result
                            $result = mysqli_query($conn, $sql);

                            // Check if the query was successful
                            if ($result) {
                                // Fetch the count from the result
                                $row = mysqli_fetch_assoc($result);
                                $count = $row['COUNT(*)'];
                                
                                // Display the count
                                echo "<p class='py-3 text-center text-8xl'>$count</p>";

                            } else {
                                // The query failed, display an error message
                                echo "Error: " . $sql . "<br>" . mysqli_error($conn);
                            }

                            // Close the MySQL connection
                            mysqli_close($conn);
                        
                        ?>

                    </div>

                    <!-- Box 3 -->
                    <div class="bg-white shadow-xl rounded-3xl p-4 border-2 border-gray-300">
                        <h1 class="mb-3 py-1 text-center font-bold text-2xl rounded-t-lg bg-gray-300"><span><i class="bi bi-clock"></i></span> Average Cycle Time (mm:ss)</h1>
                        
                        <!-- display production data -->
                        <!-- display average cycle time from cycle_time table where completed_at table date = current date -->
                        <?php
                            // open connection 
                            $conn = mysqli_connect($servername, $username, $password, $db);

                            // Select the average cycle time from the table where the date component of the datetime field is equal to the current date
                            $sql = "SELECT AVG(TIME_TO_SEC(cycle_time)) FROM completed_assemblies WHERE DATE(completed_at) = CURDATE()";

                            // Execute the query and store the result
                            $result = mysqli_query($conn, $sql);

                            // Check if the query was successful
                            if ($result) {
                                // Fetch the average cycle time from the result
                                $row = mysqli_fetch_assoc($result);
                                $avg_cycle_time = $row['AVG(TIME_TO_SEC(cycle_time))'];
                                $avg_cycle_time = gmdate("i:s", $avg_cycle_time);
                                
                                // Display the average cycle time
                                echo "<p class='py-3 text-center text-8xl'>$avg_cycle_time</p>";

                            } else {
                                // The query failed, display an error message
                                echo "Error: " . $sql . "<br>" . mysqli_error($conn);
                            }

                            // Close the MySQL connection
                            mysqli_close($conn);   
                            
                        ?>

                    </div>

                    <!-- Box 4 -->
                    <div class="bg-white shadow-xl rounded-3xl p-4 border-2 border-gray-300">
                        <h1 class="mb-3 py-1 text-center font-bold text-2xl rounded-t-lg bg-gray-300"><span><i class="bi bi-hand-thumbs-up"></i></span> Productivity score</h1>
                        
                        <!-- display production data -->
                        <p class="py-3 text-center text-8xl">87%</p>

                    </div>

                    <!-- Box 5 -->
                    <div class="bg-white shadow-xl rounded-3xl p-4 border-2 border-gray-300">
                        <h1 class="mb-3 py-1 text-center font-bold text-2xl rounded-t-lg bg-gray-300"><span><i class="bi bi-hourglass-split"></i></span> Assemblies In Progress</h1>
                        
                        <!-- display production data -->
                        <p class="py-3 text-center text-8xl">3</p>

                    </div>

                    <!-- Box 6 -->
                    <div class="bg-white shadow-xl rounded-3xl p-4 mx-h-fit border-2 border-gray-300">
                        <h1 class="mb-3 py-1 text-center font-bold text-2xl rounded-t-lg bg-gray-300"><span><i class="bi bi-exclamation-triangle"></i></span> Warnings</h1>
                        
                        <!-- display production data -->
                        <p class="pt-2 pl-2 text-left text-xl"><span><i class="bi bi-exclamation-circle-fill text-black"></i></span> Tablet 3 is not connected</p>
                        <p class="pt-2 pl-2 text-left text-xl"><span><i class="bi bi-exclamation-circle-fill text-black"></i></span> Station 2 needs more materials</p>
                        <p class="pt-2 pl-2 text-left text-xl"><span><i class="bi bi-exclamation-circle-fill text-black"></i></span> Quality percentage under 90% </p>


                    </div>

                    <!-- Box 7 -->
                    <div class="bg-white shadow-xl rounded-3xl p-4 border-2 border-gray-300">
                        <h1 class="mb-3 py-1 text-center font-bold text-2xl rounded-t-lg bg-gray-300"><span><i class="bi bi-box-seam"></i></span> Production Rate</h1>
                        
                        <!-- display production data -->
                        <p class="py-3 text-center text-8xl">1</p>

                    </div>
                </div>
            </div>
        <div>
    </section>
    



</body>


</html>