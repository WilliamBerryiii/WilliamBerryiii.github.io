---
layout: post
title: HBase, Thrift, & C# - First Scanner and Leveraging Generics
date: '2014-05-04T15:50:00.001-07:00'
author: William Berry
tags:
- Scanners
- HBase
- Thrift
- Generics
- Type Constraints
- C# NoSql
modified_time: '2014-05-17T23:38:55.705-07:00'
---

Continuing the epic series on Hbase, Thrift and C#, is this installment where 
we will review building our first row scanner by leveraging inheritance and 
generics to provide a broad based solution.  If you have not done so please 
check out the other parts of the series: 

Part 1 - [NuGet Servers, HBase, Thrift Code Generation and one sweet Jenkins CI Build](http://www.lucidmotions.net/2014/04/nuget-code-generation-jenkins-thrift-hbase.html) 
Part 2 - [HBase, Thrift & C# - First Connections](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-first-connections.html) 
Part 3 - [HBase, Thrift, & C# - Managing Sessions](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-session-management.html) 
Part 4 - [HBase, Thrift, & C# - First Scanner and Leveraging Generics](http://www.lucidmotions.net/2014/05/hbase-thrift-csharp-generic-row-scanner.html) 


Hopefully you are somewhat familiar with the concepts of No-SQL and the 
various sub-database types.  If not, I highly recommend spending an hour with 
Martin Folwer's - [Introduction To No-SQL](https://www.youtube.com/watch?v=qI_g07C_Q5I) over on YouTube.  It's an 
incredibly insightful skim of the No-Sql space. 

The Apache HBase project is a kin to the Cassandra project in that they are 
both databases oriented in the Column-Family store approach.  I am not enough 
of an expert on the topic to provide deep details, so I will leave you to your 
wits and Google to fill in any missing pieces. 

Assuming you have some data in your working HBase cluster, I know ... it's a 
hell of an assumption; but go with me on this, we will need some way to get at 
that data.  For now, we will simply focus on retreiving the data from the 
database and leave writing data for later in the series. 

The example query we will work with is the scan.   Specifically, a prefix scan 
that will return all rows where the supplied identifier is matched against row 
key prefixes. 

We will begin by building the shell of a scanner class.  It needs a few 
properties, such as the target table name, the columns we want to retrieve and 
a reference to the client we built back in [part II](https://www.blogger.com/blogger.g?blogID=4707687462195457004#editor/target=post;postID=5568222696367618036;onPublishedMenu=posts;onClosedMenu=posts;postNum=2;src=postname). 

```csharp
public class Scanner
{ 
    public string TableName { get; protected set; }
    public string[] Columns { get; protected set; }
    public Hbase.Client HBaseClient { get; set; }
 
    protected Scanner() 
    { 
 
    } 
}
```

With our class shell written, let's dig into our first public method.  The 
method will take in a row key prefix as a parameter and will return a 
List&lt;T&gt;, where T is a model of our the underlaying HBase entity, let's 
call it "Foo".  Additionally, we should tease out a private method that will 
iterate across the scanners results, yielding an IEnumerable&lt;Foo&gt;, which 
we can return as a list to the source caller. 

```csharp
public List<Foo> SelectWithPrefixScanner(string identifier)
{  
     var col = new List<byte[]>();  
     col.AddRange(Columns.Select(StaticHelpers.GetBytes));  
    
     var scanner = HBaseClient.scannerOpenWithPrefix(  
            TableName.GetBytes(),  
            identifier.GetBytes(),  
            col,  
            new Dictionary<byte[], byte[]>()  
        );  
    
     return GetAllRows<Foo>(scanner).ToList();  
} 
 
private IEnumerable<Foo> GetAllRows(int scanner)
{ 
     while (true)
     { 
          var scannerResult = HBaseClient.scannerGet(scanner); 
          if (scannerResult.Count > 0)
          { 
               var foo = new Foo() 
               { 
                   Identifier = scannerResult.First().Row.GetString(), 
                   Data = scannerResult.First().Columns 
               }; 
  
               // Take data object and run container's parser over it. 
               foo.ParseFields(); 
  
               yield return foo;
           } 
           else 
           { 
               HBaseClient.scannerClose(scanner); 
               yield break;
            } 
      } 
}
```

In the SelectWithPrefixScanner 
method, we begin by building a list of columns that we will want the scanner 
to retrieve for us.  The columns property could be set up with something as 
simple as: 

```csharp
Columns = new[] { "c:v" };
```

where "c" is the column family in the rows to be queried and "v" is the 
specific column.  Using a Linq Select(), the columns are passed to an 
extension method that will convert the strings into byte arrays adding the 
result to the "col" variable. 

Next, we set up the scanner using the HBase Client's scannerOpenWithPrefix 
method.  As I noted before, the prefix scanner will select all rows where the 
row key begins with the identifier we are passing in.  This method also 
requires a table name as bytes, the prefix identifier as bytes, our previously 
defined columns and a dictionary of attributes. 

*Moment of Honesty:  I have no clue what the available attributes are that can 
go in the scanner.  I could crack open the HBase Thrift implementation and 
find out but have not done so to date.  I have searched Google a'plenty, and 
my results have always yielded squat.  So, yeah.* 

Continuing, the call to HBaseClient.scannerOpenWithPrefix() will return an Int 
identifier which uniquely identifies the remote scanner we instantiated. The 
scanners identifier is passed to the private method which will do the heavy 
lifting to fetch the results. 

The GetAllRows() method is a simple while loop that yields the results of the 
Client's scannerGet() method.  As long as there are more results available, 
the method will build "Foo"s, using object initializer syntax to populate 
stock fields, and subsequently call a method on Foo to have the data parsed 
into fields/properties. 

And that's it.  More or less straight forward; but, we are not done quite yet. 
 Suppose for the sake of argument that we want to implement this scanner for 
not only type "Foo", but also type "Bar".  Generics should do nicely. 

Step one to making this a generic set-up, is to define a common entity 
interface.  Let's call that IHBaseEntity, and make it looks something like: 

```csharp
public interface IHBaseEntity
{ 
    string Identifier { get; set; }
    Dictionary<byte[], Hbase.TCell> Data { get; set; };
 
    void ParseFields(); 
}
```

All "Foo" and "Bar" need to do is implement the interface by providing the two 
properties and a void method that can take *Data* and parse it into the 
respective entities own properties/fields. 

The next thing we need to do is get the SelectWithPrefixScanner to work with 
generic types.  We will update the method signature to use type 'T, add type 
constraints to indicate that we are new'ing objects of type 'T and that the 
new'ed objects must implement the IHBaseEntity interface. 

```csharp
public List<T> SelectWithPrefixScanner<T>(string identifier) where T : IHBaseEntity, new() 
{ 
   var col = new List<byte[]>(); 
   col.AddRange(Columns.Select(StaticHelpers.GetBytes)); 
 
   var scanner = HBaseClient.scannerOpenWithPrefix( 
            tableName.GetBytes(), 
            identifier.GetBytes(), 
            col, 
            new Dictionary<byte[], byte[]>() 
        ); 
  
    return GetAllRows<T>(scanner).ToList(); 
}
```

Because our return type has been updated from List&lt;Foo&gt; to List&lt;T&gt; 
we will need to make similar modifications to the GetAllRows method: 

```csharp
private IEnumerable<T> GetAllRows<T>(int scanner) where T : IHBaseEntity, new() 
{ 
    while (true)
    { 
        var scannerResult = HBaseClient.scannerGet(scanner); 
        if (scannerResult.Count > 0)
        { 
            var obj = new T() 
            { 
                 Identifier = scannerResult.First().Row.GetString(), 
                 Data = scannerResult.First().Columns 
             }; 
  
             // Take data object and run container's parser over it. 
             obj.ParseFields(); 
  
             yield return obj;
         } 
         else 
         { 
              HBaseClient.scannerClose(scanner); 
              yield break;
         } 
     } 
}
```

Update with the same constraints, build new objects of type 'T instead of Foo. 
 Since we added the IHBaseEntity interface, we do not need to adjust the 
setting of Identifier and Data or the call to ParseFields. 

Lastly, implementing a custom scanner can now be as simple as setting 
properties for the specific table and columns that you want to query: 

```csharp
public class MyCustomScanner : IScanner
{ 
    public MyCustomScanner() 
        : base() 
    { 
        TableName = "my_table_name"; 
        Columns = new[] { "c:v" }; 
    } 
}
```

Through the use of generics, we have been able to make a base scanner that can 
work for any entity implementing the IHBaseEntity interface.  In the next part 
of the series we will investigate working with the entities and implementing 
the ParseFields() method.  As always, questions and comments are welcomed! 