import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

public class SmokeTest {

  @Test
  void exampleDotComReturns200() {
    given()
      .when().get("https://example.com")
      .then().statusCode(200);
  }
}
