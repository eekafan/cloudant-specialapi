# Overview
The examples for api usgae shown in the other documents are given in curl.
This section provides examples on how to invoke the api with the IBM-provided Java Cloudant client library.

# Method Invocation
Java-cloudant library supports the client.executeRequest method to perform general purpose http  requests, using a CloudantClient Class instance  

As an example, let us consider how to invoke the equivalent of the following curl command 

```
curl -u northamd:*** http://activesn.bkp.ibm.com/_api/migrate/  
diagnoosi/_design/potilaan_merkinnan_aika4 -X POST -d @ pmkc2.json
```

Build a method such as

```   
public static JsonObject postDesignDoc   
(CloudantClient client,  String cluster, String ddid, String dd_content) throws IOException {
	String url = cluster + "/_api/migrate/" + ddid;
	HttpConnection response =  
	 client.executeRequest(Http.POST(new URL(url), "application/json").setRequestBody(dd_content));
                 JsonObject result = (JsonObject) new JsonParser().parse(response.responseAsString());
                 response.disconnect();
 if (result.isJsonObject()){ return result; }
 else {return null;}
}
```   

Find the cluster and designdoc content into strings
and then call the method

```
JsonObject jobsubmit_response = postDesignDoc(thisClient,cluster,ddid,pmkc2);
```

then the result will be a JsonObject class with the job json returned by the api.

You can then invoke a GET on this job-document via executeRequest again such as....

```
String url = cluster + "/_api/migrate/" +   
jobsubmit_response. get("id").getAsString();

HttpConnection response = client.executeRequest(Http.GET(new URL(url);
JsonObject result = (JsonObject) new JsonParser().  
parse(response.responseAsString());
```


